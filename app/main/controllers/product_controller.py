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

import pprint


def get_products():
    name = request.args.get("name")
    category_id = request.args.get("category_id")
    limit = request.args.get("limit", type=int)
    include = request.args.get("include", "inventories.io_history").split(',')

    include_filters = {}
    
    if include:
        if 'inventories' in include:
            include_filters['inventories'] = ProductInventoryFilter()

        elif 'inventories.io_history' in include:
            start_date = request.args.get("start_date", date.today().strftime("%Y-%m-%d"))
            end_date = request.args.get("end_date")

            start_date = parser.parse(start_date, fuzzy=True)

            if start_date and not end_date:
                end_date = start_date - timedelta(days=20)
                end_date = end_date.strftime("%Y-%m-%d")

            end_date = parser.parse(end_date, fuzzy=True)

            if end_date < start_date:
                start_date, end_date = end_date, start_date

            start_date = start_date.strftime("%Y-%m-%d")
            end_date = end_date.strftime("%Y-%m-%d")

            include_filters['inventories'] = ProductInventoryFilter(include={
                'io_history': ProductIOHistoryFilter(start_date=start_date, end_date=end_date)
            })

    product_filter = ProductFilter(name, category_id, limit, include_filters)
    products = ProductService.get_all_products(product_filter)
    json_products = [product.as_dict() for product in products]

    if request.accept_mimetypes.best == "application/json":
        return jsonify(json_products)

    return render_inertia(component_name="ProductsList", props={"products": json_products})
