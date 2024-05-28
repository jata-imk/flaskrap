from datetime import datetime
from app import db

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(127), nullable=False, default='')
    description = db.Column(db.String(255), nullable=False, default='')
    sku = db.Column(db.String(63), nullable=False, unique=True)
    small_image = db.Column(db.String(127), nullable=False, default='')
    out_of_stock = db.Column(db.Boolean, nullable=False, default=False)
    categories_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    category = db.relationship('Category', backref=db.backref('products', lazy=True))
    brand = db.relationship('Brand', backref=db.backref('products', lazy=True))

    def __repr__(self):
        return f'<Product {self.name}>'
