from app import db
from datetime import datetime
from sqlalchemy import func

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    min_stock_level = db.Column(db.Integer, default=10)
    barcode = db.Column(db.String(20), unique=True)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    @property
    def stock_status(self):
        if self.quantity == 0:
            return 'out-of-stock'
        elif self.quantity <= self.min_stock_level:
            return 'low-stock'
        else:
            return 'in-stock'
    
    @property
    def stock_status_text(self):
        if self.quantity == 0:
            return 'Out of Stock'
        elif self.quantity <= self.min_stock_level:
            return 'Low Stock'
        else:
            return 'In Stock'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'price': self.price,
            'quantity': self.quantity,
            'min_stock_level': self.min_stock_level,
            'barcode': self.barcode,
            'image_url': self.image_url,
            'stock_status': self.stock_status,
            'stock_status_text': self.stock_status_text,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<Category {self.name}>'
