from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import Product, Category
from sqlalchemy import or_, func

@app.route('/')
def index():
    # Get search and filter parameters
    search = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    stock_filter = request.args.get('stock', '')
    sort_by = request.args.get('sort', 'name')
    
    # Build query
    query = Product.query
    
    # Apply search filter
    if search:
        query = query.filter(or_(
            Product.name.contains(search),
            Product.description.contains(search),
            Product.barcode.contains(search)
        ))
    
    # Apply category filter
    if category_filter:
        query = query.filter(Product.category == category_filter)
    
    # Apply stock filter
    if stock_filter == 'low':
        query = query.filter(Product.quantity <= Product.min_stock_level)
    elif stock_filter == 'out':
        query = query.filter(Product.quantity == 0)
    elif stock_filter == 'in':
        query = query.filter(Product.quantity > Product.min_stock_level)
    
    # Apply sorting
    if sort_by == 'name':
        query = query.order_by(Product.name)
    elif sort_by == 'price':
        query = query.order_by(Product.price)
    elif sort_by == 'quantity':
        query = query.order_by(Product.quantity.desc())
    elif sort_by == 'category':
        query = query.order_by(Product.category, Product.name)
    
    products = query.all()
    
    # Get all categories for filter dropdown
    categories = db.session.query(Product.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('index.html', 
                         products=products, 
                         categories=categories,
                         search=search,
                         category_filter=category_filter,
                         stock_filter=stock_filter,
                         sort_by=sort_by)

@app.route('/dashboard')
def dashboard():
    # Calculate statistics
    total_products = Product.query.count()
    total_value = db.session.query(func.sum(Product.price * Product.quantity)).scalar() or 0
    low_stock_count = Product.query.filter(Product.quantity <= Product.min_stock_level).count()
    out_of_stock_count = Product.query.filter(Product.quantity == 0).count()
    
    # Category statistics
    category_stats = db.session.query(
        Product.category,
        func.count(Product.id).label('count'),
        func.sum(Product.quantity).label('total_quantity'),
        func.sum(Product.price * Product.quantity).label('total_value')
    ).group_by(Product.category).all()
    
    # Recent products (last 10 added)
    recent_products = Product.query.order_by(Product.created_at.desc()).limit(10).all()
    
    # Low stock products
    low_stock_products = Product.query.filter(
        Product.quantity <= Product.min_stock_level,
        Product.quantity > 0
    ).order_by(Product.quantity).limit(10).all()
    
    return render_template('dashboard.html',
                         total_products=total_products,
                         total_value=total_value,
                         low_stock_count=low_stock_count,
                         out_of_stock_count=out_of_stock_count,
                         category_stats=category_stats,
                         recent_products=recent_products,
                         low_stock_products=low_stock_products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        try:
            product = Product(
                name=request.form['name'],
                description=request.form['description'],
                category=request.form['category'],
                price=float(request.form['price']),
                quantity=int(request.form['quantity']),
                min_stock_level=int(request.form['min_stock_level']),
                barcode=request.form['barcode'] if request.form['barcode'] else None,
                image_url=request.form['image_url'] if request.form['image_url'] else None
            )
            
            db.session.add(product)
            db.session.commit()
            flash(f'Product "{product.name}" added successfully!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding product: {str(e)}', 'error')
    
    # Get existing categories for dropdown
    categories = db.session.query(Product.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('add_product.html', categories=categories)

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        try:
            product.name = request.form['name']
            product.description = request.form['description']
            product.category = request.form['category']
            product.price = float(request.form['price'])
            product.quantity = int(request.form['quantity'])
            product.min_stock_level = int(request.form['min_stock_level'])
            product.barcode = request.form['barcode'] if request.form['barcode'] else None
            product.image_url = request.form['image_url'] if request.form['image_url'] else None
            
            db.session.commit()
            flash(f'Product "{product.name}" updated successfully!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating product: {str(e)}', 'error')
    
    # Get existing categories for dropdown
    categories = db.session.query(Product.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('edit_product.html', product=product, categories=categories)

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        product_name = product.name
        db.session.delete(product)
        db.session.commit()
        flash(f'Product "{product_name}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting product: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/api/products')
def api_products():
    """API endpoint for getting products as JSON"""
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@app.route('/api/products/<int:product_id>')
def api_product(product_id):
    """API endpoint for getting a single product as JSON"""
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())
