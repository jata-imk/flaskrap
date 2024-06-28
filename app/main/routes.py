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
    products = product_controller.get_products()    
    json_products = [product.as_dict() for product in products]

    return render_inertia(
        component_name="ProductsList",
        props={
            "products": json_products
        }
    )
