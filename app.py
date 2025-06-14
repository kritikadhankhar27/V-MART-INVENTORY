from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# ------------------ DATABASE ------------------

def get_db():
    """Get database connection with row factory for easier access"""
    conn = sqlite3.connect('v_mart.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables and sample data"""
    conn = get_db()
    c = conn.cursor()

    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS Categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS Suppliers (
            supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT,
            email TEXT,
            address TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            category_id INTEGER,
            supplier_id INTEGER,
            price REAL NOT NULL CHECK(price > 0),
            stock_quantity INTEGER NOT NULL CHECK(stock_quantity >= 0),
            min_stock_level INTEGER DEFAULT 10,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES Categories(category_id),
            FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
        )
    ''')

    # Insert initial data if empty
    c.execute('SELECT COUNT(*) FROM Categories')
    if c.fetchone()[0] == 0:
        categories = [
            ('Fruits',), ('Vegetables',), ('Dairy',), ('Bakery',), 
            ('Beverages',), ('Meat & Poultry',), ('Frozen Foods',), ('Snacks',)
        ]
        c.executemany('INSERT INTO Categories (name) VALUES (?)', categories)

    c.execute('SELECT COUNT(*) FROM Suppliers')
    if c.fetchone()[0] == 0:
        suppliers = [
            ('Fresh Farms Ltd.', '9876543210', 'farm@freshfarms.com', '123 Farm Road'),
            ('Dairy Pure', '9876543211', 'info@dairypure.com', '456 Dairy Lane'),
            ('Bakery Express', '9876543212', 'orders@bakeryexpress.com', '789 Baker Street'),
            ('Beverage Co.', '9876543213', 'sales@beverageco.com', '321 Drink Ave'),
        ]
        c.executemany('INSERT INTO Suppliers (name, contact, email, address) VALUES (?, ?, ?, ?)', suppliers)

    c.execute('SELECT COUNT(*) FROM Products')
    if c.fetchone()[0] == 0:
        products = [
            ('Apple', 'Fresh red apples', 1, 1, 2.50, 100, 15),
            ('Banana', 'Yellow bananas', 1, 1, 1.20, 80, 20),
            ('Milk', 'Fresh whole milk', 3, 2, 3.50, 50, 10),
            ('Bread', 'Whole wheat bread', 4, 3, 2.00, 30, 5),
            ('Orange Juice', 'Fresh orange juice', 5, 4, 4.00, 40, 8),
            ('Carrot', 'Fresh carrots', 2, 1, 0.80, 70, 25),
            ('Chicken Breast', 'Fresh chicken breast', 6, 1, 8.99, 25, 5),
            ('Frozen Pizza', 'Pepperoni pizza', 7, 3, 6.99, 15, 3),
        ]
        c.executemany('''
            INSERT INTO Products (name, description, category_id, supplier_id, price, stock_quantity, min_stock_level)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', products)

    conn.commit()
    conn.close()

# ------------------ HELPER FUNCTIONS ------------------

def get_product_with_details(product_id):
    """Get product with category and supplier details"""
    conn = get_db()
    product = conn.execute('''
        SELECT p.*, c.name AS category_name, s.name AS supplier_name
        FROM Products p
        LEFT JOIN Categories c ON p.category_id = c.category_id
        LEFT JOIN Suppliers s ON p.supplier_id = s.supplier_id
        WHERE p.product_id = ?
    ''', (product_id,)).fetchone()
    conn.close()
    return product

def get_all_products(search_term=None, category_filter=None, sort_by='name', sort_order='asc'):
    """Get all products with optional filtering and sorting"""
    conn = get_db()
    
    query = '''
        SELECT p.*, c.name AS category_name, s.name AS supplier_name
        FROM Products p
        LEFT JOIN Categories c ON p.category_id = c.category_id
        LEFT JOIN Suppliers s ON p.supplier_id = s.supplier_id
        WHERE 1=1
    '''
    params = []
    
    if search_term:
        query += ' AND (p.name LIKE ? OR p.description LIKE ?)'
        params.extend([f'%{search_term}%', f'%{search_term}%'])
    
    if category_filter:
        query += ' AND p.category_id = ?'
        params.append(category_filter)
    
    # Add sorting
    valid_sort_columns = ['name', 'price', 'stock_quantity', 'category_name']
    if sort_by in valid_sort_columns:
        if sort_by == 'category_name':
            sort_column = 'c.name'
        else:
            sort_column = f'p.{sort_by}'
        
        sort_direction = 'DESC' if sort_order.lower() == 'desc' else 'ASC'
        query += f' ORDER BY {sort_column} {sort_direction}'
    
    products = conn.execute(query, params).fetchall()
    conn.close()
    return products

# ------------------ ROUTES ------------------

@app.route('/')
def index():
    """Main inventory page with search and filter functionality"""
    search_term = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    sort_by = request.args.get('sort', 'name')
    sort_order = request.args.get('order', 'asc')
    
    products = get_all_products(search_term, category_filter, sort_by, sort_order)
    
    # Get categories for filter dropdown
    conn = get_db()
    categories = conn.execute('SELECT * FROM Categories ORDER BY name').fetchall()
    conn.close()
    
    # Calculate low stock count for badge
    low_stock_count = len([p for p in products if p['stock_quantity'] <= p['min_stock_level']])
    
    return render_template('index.html', 
                         products=products, 
                         categories=categories,
                         search_term=search_term,
                         category_filter=category_filter,
                         sort_by=sort_by,
                         sort_order=sort_order,
                         low_stock_count=low_stock_count)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    """Add new product"""
    if request.method == 'POST':
        try:
            conn = get_db()
            conn.execute('''
                INSERT INTO Products (name, description, category_id, supplier_id, price, stock_quantity, min_stock_level)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                request.form['name'].strip(),
                request.form['description'].strip(),
                request.form['category_id'],
                request.form['supplier_id'],
                float(request.form['price']),
                int(request.form['stock_quantity']),
                int(request.form.get('min_stock_level', 10))
            ))
            conn.commit()
            conn.close()
            flash('Product added successfully!', 'success')
            return redirect(url_for('index'))
        except ValueError as e:
            flash('Invalid input. Please check your data.', 'error')
        except sqlite3.Error as e:
            flash(f'Database error: {str(e)}', 'error')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
    
    # Get categories and suppliers for dropdowns
    conn = get_db()
    categories = conn.execute('SELECT * FROM Categories ORDER BY name').fetchall()
    suppliers = conn.execute('SELECT * FROM Suppliers ORDER BY name').fetchall()
    conn.close()
    
    return render_template('add_product.html', categories=categories, suppliers=suppliers)

@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    """Edit existing product"""
    if request.method == 'POST':
        try:
            conn = get_db()
            conn.execute('''
                UPDATE Products 
                SET name = ?, description = ?, category_id = ?, supplier_id = ?, 
                    price = ?, stock_quantity = ?, min_stock_level = ?, updated_at = CURRENT_TIMESTAMP
                WHERE product_id = ?
            ''', (
                request.form['name'].strip(),
                request.form['description'].strip(),
                request.form['category_id'],
                request.form['supplier_id'],
                float(request.form['price']),
                int(request.form['stock_quantity']),
                int(request.form.get('min_stock_level', 10)),
                product_id
            ))
            conn.commit()
            conn.close()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('index'))
        except ValueError as e:
            flash('Invalid input. Please check your data.', 'error')
        except sqlite3.Error as e:
            flash(f'Database error: {str(e)}', 'error')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
    
    # Get product details
    product = get_product_with_details(product_id)
    if not product:
        flash('Product not found.', 'error')
        return redirect(url_for('index'))
    
    # Get categories and suppliers for dropdowns
    conn = get_db()
    categories = conn.execute('SELECT * FROM Categories ORDER BY name').fetchall()
    suppliers = conn.execute('SELECT * FROM Suppliers ORDER BY name').fetchall()
    conn.close()
    
    return render_template('edit_product.html', product=product, categories=categories, suppliers=suppliers)

@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    """Delete product"""
    try:
        conn = get_db()
        # Check if product exists
        product = conn.execute('SELECT name FROM Products WHERE product_id = ?', (product_id,)).fetchone()
        if product:
            conn.execute('DELETE FROM Products WHERE product_id = ?', (product_id,))
            conn.commit()
            flash(f'Product "{product["name"]}" deleted successfully!', 'success')
        else:
            flash('Product not found.', 'error')
        conn.close()
    except sqlite3.Error as e:
        flash(f'Database error: {str(e)}', 'error')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/low_stock')
def low_stock():
    """Low stock report with enhanced visualization"""
    conn = get_db()
    products = conn.execute('''
        SELECT p.*, c.name AS category_name, s.name AS supplier_name
        FROM Products p
        LEFT JOIN Categories c ON p.category_id = c.category_id
        LEFT JOIN Suppliers s ON p.supplier_id = s.supplier_id
        WHERE p.stock_quantity <= p.min_stock_level
        ORDER BY (p.stock_quantity * 1.0 / p.min_stock_level) ASC
    ''').fetchall()
    conn.close()
    
    return render_template('low_stock.html', products=products)

@app.route('/api/stock_levels')
def api_stock_levels():
    """API endpoint for stock level data (for charts)"""
    conn = get_db()
    data = conn.execute('''
        SELECT c.name AS category, 
               COUNT(p.product_id) AS total_products,
               SUM(CASE WHEN p.stock_quantity <= p.min_stock_level THEN 1 ELSE 0 END) AS low_stock_products
        FROM Categories c
        LEFT JOIN Products p ON c.category_id = p.category_id
        GROUP BY c.category_id, c.name
        ORDER BY c.name
    ''').fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in data])

# ------------------ ERROR HANDLERS ------------------

@app.errorhandler(404)
def not_found_error(error):
    return render_template('base.html', content='<div class="alert alert-danger">Page not found.</div>'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('base.html', content='<div class="alert alert-danger">Internal server error.</div>'), 500

# ------------------ MAIN ------------------

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)

# Initialize database when module is imported
try:
    init_db()
except Exception as e:
    print(f"Database initialization error: {e}")
    # Create a minimal fallback to ensure the app can start
    pass
