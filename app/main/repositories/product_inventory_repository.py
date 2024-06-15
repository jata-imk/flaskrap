from app import db
from app.main.models import ProductInventory

class ProductInventoryRepository:
    @staticmethod
    def get_by_product(id):
        return db.session.query(ProductInventory).filter_by(product_id=id).first()
    
    @staticmethod
    def create(product_inventory):
        db.session.add(product_inventory)
        db.session.commit()

    @staticmethod
    def update(product_inventory):
        db.session.commit()
