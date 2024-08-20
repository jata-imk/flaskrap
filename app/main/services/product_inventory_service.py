from app.main.repositories.product_inventory_repository import (
    ProductInventoryRepository,
)
from app.main.repositories.product_io_history_repository import (
    ProductIOHistoryRepository,
)
from app.main.models.ProductIOHistory import ProductIOHistory


class ProductInventoryService:
    @staticmethod
    def get_inventories(filter = None):
        return ProductInventoryRepository.get_all(filter)

    @staticmethod
    def log_io_transaction(inventory_id, io_type, quantity, price):
        history = ProductIOHistory(
            inventory_id=inventory_id, io_type=io_type, quantity=quantity, price=price
        )
        ProductIOHistoryRepository.create(history)
