import json
import math
import re
from dateutil import parser
from datetime import date, timedelta

from flask import request, jsonify
from flask_inertia import render_inertia

from app.main.dtos.images_filter.image_filter import ImageFilter
from app.main.dtos.images_filter.pivot_image_filter import PivotImageFilter
from app.main.repositories.product_inventory_repository import (
    ProductInventoryRepository,
)
from app.main.repositories.product_io_history_repository import (
    ProductIOHistoryRepository,
)
from app.main.services.product_service import ProductService
from app.main.dtos.product.product_filter_dto import ProductFilter

from app.main.services.product_inventory_service import ProductInventoryService
from app.main.dtos.product_inventory.product_inventory_filter_dto import (
    ProductInventoryFilter,
)
from app.main.dtos.product_io_history.product_io_history_filter_dto import (
    ProductIOHistoryFilter,
)

from app.main.repositories.prompt_history_repository import PromptHistoryRepository
from app.main.services.external.google_gemini_service import GoogleGeminiService
from app.main.use_cases.request_prompt_for_product import RequestPromptForProductUseCase


def get_products():
    try:
        name = request.args.get("name")
        category_id = request.args.get("category_id")
        page = request.args.get("page", type=int, default=1)
        page_size = request.args.get("page_size", type=int, default=10)
        include = parse_include(request.args.get("include", "images,inventories.io_history"))

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

            if "images" in include:
                include_filters["images"] = PivotImageFilter(
                    is_primary=True
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
    """
    Parsea el parámetro 'include' para construir un diccionario con relaciones, campos y filtros.
    
    Ejemplo de entrada:
    "images,inventories.io_history(id,transaction_date,price):{start_date=2024-10-01,end_date=2024-10-21}"
    
    Ejemplo de salida:
    {
        "images": {
            "fields": null,
            "filters": null
        },
        "inventories": {
            "fields": null,
            "filters": null
        },
        "io_history": {
            "fields": ["id", "transaction_date", "price"],
            "filters": {
                "start_date": "2024-10-01",
                "end_date": "2024-10-21"
            }
        }
    }
    """
    if not include_str:
        return {}

    # Expresión regular para relaciones con posibles campos y filtros
    pattern = r'([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)?)(?:\(([^)]*)\))?(?::\{([^}]*)\})?'

    matches = re.findall(pattern, include_str)
    result = {}

    for relation, fields, filters in matches:
        # Procesar campos (si existen)
        fields_list = [field.strip() for field in fields.split(",")] if fields else None
        
        # Procesar filtros (si existen)
        filters_dict = {}
        if filters:
            for filter_item in filters.split(","):
                key, value = filter_item.split("=")
                filters_dict[key.strip()] = value.strip()

        # Separar relaciones anidadas
        relation_parts = relation.split(".")
        if len(relation_parts) > 1:
            # Relación anidada (última parte es la relación hija)
            parent, child = relation_parts
            if parent not in result:
                result[parent] = {"fields": None, "filters": None}
            result[child] = {"fields": fields_list, "filters": filters_dict}
        else:
            # Relación principal
            result[relation] = {"fields": fields_list, "filters": filters_dict}

    return result


def get_ai_price_analysis(product_id, inventory_id=None):
    google_gemini_service = GoogleGeminiService()
    prompt_history_repository = PromptHistoryRepository()

    google_gemini_service.init_service()
    google_gemini_service.set_model(
        model_name="gemini-1.5-flash",
        system_instructions="Actúa como un agente de ventas que en base a la información de un historial de precios de un producto indica si es mejor comprar ahora o esperar. Si se sugiere esperar, proporciona una estimación de cuánto tiempo esperar.",
    )

    end_date = date.today().strftime("%Y-%m-%d")
    start_date = (date.today() - timedelta(days=180)).strftime("%Y-%m-%d")

    if inventory_id is None:
        inventory_id = ProductInventoryRepository.get_by_product_id(product_id)["id"]

    historial_precios = ProductIOHistoryRepository.get_all(
        ProductIOHistoryFilter(
            inventory_id=inventory_id,
            start_date=start_date,
            end_date=end_date,
        )
    )

    historial_precios = historial_precios[::-1]
    historial_precios_formatted = [
        {
            "date": historial_precios_row.transaction_date.strftime("%Y-%m-%d"),
            "price": f"${historial_precios_row.price:.2f}" if historial_precios_row.price else None,
        }
        for historial_precios_row in historial_precios
    ]

    prompt = """
        {
            "product_price_history": %s,
            "instructions": {
            "fill_missing_prices": "Completa los registros de fechas faltantes usando el precio más cercano anterior.",
            "analyze_trend": "Analiza el comportamiento del precio a lo largo del tiempo y determina cualquier patrón o tendencia.",
            "generate_comments": "Comenta sobre el comportamiento general del precio, incluyendo subidas o bajadas relevantes.",
            "predict_future": {
                "1_week": "Genera una predicción del precio a una semana si es posible.",
                "1_month": "Genera una predicción del precio a un mes si es posible."
            },
        }
    """ % json.dumps(
        historial_precios_formatted, indent=4
    )

    useCase = RequestPromptForProductUseCase(
        gemini_service=google_gemini_service,
        prompt_history_repository=prompt_history_repository,
    )

    prompt_history_register = useCase.execute(
        product_id=product_id,
        prompt=prompt,
    )

    if request.accept_mimetypes.best == "application/json":
        return jsonify(prompt_history_register.as_dict())
