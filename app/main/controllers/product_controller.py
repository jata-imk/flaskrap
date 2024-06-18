from flask import render_template
from app.main.services.product_service import ProductService

def get_products():
    products = ProductService.get_all_products()
    return render_template('products/products.html', products=products)
