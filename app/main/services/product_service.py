# app/main/services/product_service.py

from app.main.repositories.product_inventory_repository import ProductInventoryRepository
from app.main.repositories.product_repository import ProductRepository
from app.main.repositories.category_repository import CategoryRepository
from app.main.repositories.brand_repository import BrandRepository
from app.main.repositories.vendor_repository import VendorRepository
from app.main.models import Product, Category, Brand, ProductInventory, Vendor

class ProductService:
    @staticmethod
    def create_product(product_data):
        category = CategoryRepository.get_by_name(product_data['category'])
        if not category:
            category = Category(name=product_data['category'])
            CategoryRepository.create(category)

        brand = BrandRepository.get_by_name(product_data['brand'])
        if not brand:
            brand = Brand(name=product_data['brand'])
            BrandRepository.create(brand)

        vendor = VendorRepository.get_by_name(product_data['vendor'])
        if not vendor:
            vendor = Vendor(name=product_data['vendor'])
            VendorRepository.create(vendor)

        product = Product(
            name=product_data['name'],
            description=product_data['description'],
            # sku=product_data['sku'], Se debe generar un sku propio
            category_id=category.id,
            brand_id=brand.id,
        )
        ProductRepository.create(product)

    @staticmethod
    def create_or_update_product(product_data):
        product = ProductRepository.get_by_name(product_data['name'])
        if not product:
            ProductService.create_product(product_data)
        else:
            # Actualiza el producto existente si es necesario
            product.price = product_data['price']
            ProductRepository.update(product)

    @staticmethod
    def get_or_create_product(product_data):
        product = ProductRepository.get_by_name(product_data['name'])
        if not product:
            ProductService.create_product(product_data)
            product = ProductRepository.get_by_name(product_data['name'])

            product_inventory = ProductInventory(
                linked_product_id=product.id,
                linked_vendor_id=product.vendor_id,
                price=0,
                quantity=0,
                sku=product_data['vendor_sku'],
            )

            ProductInventoryRepository.create(product_inventory)

        return product
