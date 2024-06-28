from app.main.repositories.product_io_history_repository import ProductIOHistoryRepository
from app.main.models.ProductIOHistory import ProductIOHistory

class InventoryService:
    @staticmethod
    def log_io_transaction(inventory_id, io_type, quantity, price):
        history = ProductIOHistory(
            inventory_id=inventory_id,
            io_type=io_type,
            quantity=quantity,
            price=price
        )
        ProductIOHistoryRepository.create(history)
