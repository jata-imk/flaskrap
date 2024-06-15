from app.main.models import ProductIOHistory
from app import db

class ProductIOHistoryRepository:
    @staticmethod
    def create(history):
        db.session.add(history)
        db.session.commit()

    @staticmethod
    def get_by_inventory_id(inventory_id):
        return db.session.query(ProductIOHistory).filter_by(inventory_id=inventory_id).all()
