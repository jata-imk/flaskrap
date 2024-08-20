# app/main/services/product_service.py

from app.main.repositories.product_inventory_repository import (
    ProductInventoryRepository,
)
from app.main.repositories.product_repository import ProductRepository
from app.main.repositories.category_repository import CategoryRepository
from app.main.repositories.brand_repository import BrandRepository
from app.main.repositories.vendor_repository import VendorRepository
from app.main.models.Product import Product
from app.main.models.Brand import Brand
from app.main.models.ProductInventory import ProductInventory
from app.main.models.Vendor import Vendor


class ProductService:
    @staticmethod
    def create_product(product_data):
        categories = product_data.get("categories", [])
        parent_category = None
        for display_text in categories:
            category = CategoryRepository.get_or_create(display_text, parent_category)
            parent_category = category

        brand = BrandRepository.get_by_name(product_data["brand"])
        if not brand:
            brand = Brand(name=product_data["brand"])
            BrandRepository.create(brand)

        vendor = VendorRepository.get_by_name(product_data["vendor"])
        if not vendor:
            vendor = Vendor(name=product_data["vendor"])
            VendorRepository.create(vendor)

        product = Product(
            name=product_data["name"],
            description=product_data.get("description", ""),
            sku=product_data["sku"],  # Se debe generar un sku propio
            categories_id=parent_category.id,
            brand_id=brand.id,
        )
        ProductRepository.create(product)

    @staticmethod
    def get_or_create_product(product_data):
        product = ProductRepository.get_by_name(product_data["name"])
        if not product:
            ProductService.create_product(product_data)
            product = ProductRepository.get_by_name(product_data["name"])

        return product

    @staticmethod
    def get_or_create_product_inventory(product_data):
        product = ProductRepository.get_by_name(product_data["name"])
        if not product:
            ProductService.create_product(product_data)
            product = ProductRepository.get_by_name(product_data["name"])

        product_inventory = ProductInventoryRepository.get_by_product_id(product.id)
        if not product_inventory:
            product_inventory = ProductInventory(
                linked_product_id=product.id,
                linked_vendor_id=VendorRepository.get_by_name(
                    product_data["vendor"]
                ).id,
                quantity=1,  # Ejemplo: 1 unidad
                price=product_data["price"],
                sku=product_data["vendor_sku"],
            )
            ProductInventoryRepository.create(product_inventory)

        return product_inventory

    @staticmethod
    def get_all_products(filter=None):
        return ProductRepository.get_all(filter)
