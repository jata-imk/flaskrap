from flask_inertia import render_inertia

from app.main import main
from app.main.controllers import product_controller


@main.route("/")
def index():
    """An endpoint to test inertia integration."""
    data = {
        "username": "foo",
        "login": "bar",
    }

    return render_inertia(
        component_name="App",
        props=data,
    )


@main.route("/products", methods=["GET"])
def products():
    return product_controller.get_products()

# TODO: Add io history endpoint
@main.route("/products/<product_id>", methods=["GET"])
def product(product_id):
    return product_controller.get_product(product_id)