from flask import request, jsonify
from flask_inertia import render_inertia

from dateutil import parser
from datetime import date, timedelta

from app.main.services.product_service import ProductService
from app.main.dtos.product.product_filter_dto import ProductFilter
from app.main.dtos.product_io_history.product_io_history_filter_dto import ProductIOHistoryFilter

from app.main.services.product_inventory_service import ProductInventoryService
from app.main.dtos.product_inventory.product_inventory_filter_dto import (
    ProductInventoryFilter,
)


def get_products():
    name = request.args.get("name")
    category_id = request.args.get("category_id")
    limit = request.args.get("limit", type=int)
    include = request.args.get("include", "inventories,io_history")
    
    # if include:
    #     include = include.split(",")

    #     if 'inventory' in include:
    #         products_id = [product.id for product in products]
    #         inventories_filter = ProductInventoryFilter(product_id=products_id)

    #         include_filters['inventory'] = inventories_filter

            # if 'io_history' in include:
            #     start_date = request.args.get("start_date", date.today().strftime("%Y-%m-%d"))
            #     end_date = request.args.get("end_date")

            #     start_date = parser.parse(start_date, fuzzy=True)

            #     if start_date and not end_date:
            #         end_date = start_date - timedelta(days=21)
            #         end_date = end_date.strftime("%Y-%m-%d")

            #     end_date = parser.parse(end_date, fuzzy=True)

            #     if end_date < start_date:
            #         start_date, end_date = end_date, start_date

            #     start_date = start_date.strftime("%Y-%m-%d")
            #     end_date = end_date.strftime("%Y-%m-%d")

            #     io_history_filter = ProductIOHistoryFilter(inventory_id=products_id, start_date=start_date, end_date=end_date)

    product_filter = ProductFilter(name, category_id, limit, include)
    products = ProductService.get_all_products(product_filter)
    json_products = [product.as_dict() for product in products]

    if request.accept_mimetypes.best == "application/json":
        return jsonify(json_products)

    return render_inertia(component_name="ProductsList", props={"products": json_products})
