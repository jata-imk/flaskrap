from app.main.services.product_service import ProductService

def get_products():
    return ProductService.get_all_products()