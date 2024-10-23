import math
from dateutil import parser
from datetime import date, timedelta

from flask import request, jsonify
from flask_inertia import render_inertia

from app.main.services.product_service import ProductService
from app.main.dtos.product.product_filter_dto import ProductFilter

from app.main.services.product_inventory_service import ProductInventoryService
from app.main.dtos.product_inventory.product_inventory_filter_dto import (
    ProductInventoryFilter,
)
from app.main.dtos.product_io_history.product_io_history_filter_dto import (
    ProductIOHistoryFilter,
)


def get_products():
    try:
        name = request.args.get("name")
        category_id = request.args.get("category_id")
        page = request.args.get("page", type=int, default=1)
        page_size = request.args.get("page_size", type=int, default=10)
        include = parse_include(request.args.get("include", "inventories.io_history"))

        include_filters = {}

        if include:
            if "inventories" in include:
                include_filters["inventories"] = ProductInventoryFilter()
                if "io_history" in include:
                    start_date, end_date = get_or_create_dates_from_dict(
                        include["io_history"]["filters"]
                    )

                    include_filters["inventories"] = ProductInventoryFilter(
                        include={
                            "io_history": ProductIOHistoryFilter(
                                start_date=start_date, end_date=end_date
                            )
                        }
                    )

        product_filter = ProductFilter(
            id=None,
            name=name,
            category_id=category_id,
            page=page,
            page_size=page_size,
            include=include_filters,
        )
        products = ProductService.get_all_products(product_filter)
        json_products = [product.as_dict() for product in products]

        total_products_count = ProductService.get_all_products_count(product_filter)
        pagination_info = {
            "total_records": total_products_count,
            "current_page": page,
            "page_size": page_size,
            "total_pages": math.ceil(total_products_count / page_size),
            "next_page": page + 1 if page * page_size < total_products_count else None,
            "previous_page": page - 1 if page > 1 else None,
        }

        if request.accept_mimetypes.best == "application/json":
            return jsonify(
                {"data": {"products": json_products}, "pagination": pagination_info}
            )

        return render_inertia(
            component_name="ProductsList",
            props={"products": json_products, "pagination": pagination_info},
        )

    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_product(product_id):
    include = parse_include(request.args.get("include", "inventories.io_history"))
    start_date, end_date = get_or_create_dates_from_dict(
        include["io_history"]["filters"]
    )

    include_filters = {
        "inventories": ProductInventoryFilter(
            include={
                "io_history": ProductIOHistoryFilter(
                    start_date=start_date, end_date=end_date
                )
            }
        )
    }
    product_filter = ProductFilter(id=product_id, include=include_filters)
    product = ProductService.get_all_products(product_filter)

    if not product:
        return jsonify({"message": "Product not found"}), 404

    json_product = product[0].as_dict()

    if request.accept_mimetypes.best == "application/json":
        return jsonify(json_product)

    return render_inertia(
        component_name="ProductDetails", props={"product": json_product}
    )


def get_or_create_dates_from_dict(dict: dict = None):
    if not dict:
        dict = {}

    start_date = dict.get("start_date", date.today().strftime("%Y-%m-%d"))
    end_date = dict.get("end_date")

    start_date = parser.parse(start_date, fuzzy=True)

    if start_date and not end_date:
        end_date = start_date - timedelta(days=20)
        end_date = end_date.strftime("%Y-%m-%d")

    end_date = parser.parse(end_date, fuzzy=True)

    if end_date < start_date:
        start_date, end_date = end_date, start_date

    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    return start_date, end_date


def parse_include(include_str):
    include = {}
    if include_str:
        relationships = include_str.split(".")
        for relation in relationships:
            fields = None
            filters = None
            rel_name = relation

            if "(" in relation and ")" in relation:
                fields = relation.split("(")[-1].split(")")[0].split(",")

            if ":" in relation:
                filters_string = relation.split(":")[-1]

                filters = (
                    [f.split("=") for f in filters_string.lstrip(":").split(",")]
                    if filters_string
                    else filters
                )
                filters = dict(filters) if (len(filters)) else filters

            if fields:
                rel_name = relation.split("(")[0]
            elif filters:
                rel_name = relation.split(":")[0]

            include[rel_name] = {"fields": fields, "filters": filters}

    return include
