from flask import render_template

from app.main import main
from app.main.controllers import product_controller


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/products', methods=['GET'])
def products():
    return product_controller.get_products()