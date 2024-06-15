from flask import render_template
from app.main import main

from app.main.repositories.product_repository import ProductRepository


@main.route('/')
def index():
    product = ProductRepository.get_by_name('PlayStation 5')

    if not product:
        return 'No se encontro el producto'
    
    return 'Si'