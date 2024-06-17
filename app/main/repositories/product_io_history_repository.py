from app import db
from app.main.models.ProductIOHistory import ProductIOHistory

class ProductIOHistoryRepository:
    @staticmethod
    def create(history):
        db.session.add(history)
        db.session.commit()

    @staticmethod
    def get_by_inventory_id(inventory_id):
        return db.session.query(ProductIOHistory).filter_by(inventory_id=inventory_id).all()
