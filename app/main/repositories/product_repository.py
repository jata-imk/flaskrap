from app import db
from app.main.models.Product import Product

class ProductRepository:
    @staticmethod
    def get_by_name(name):
        return db.session.query(Product).filter_by(name=name).first()

    @staticmethod
    def create(product):
        db.session.add(product)
        db.session.commit()

    @staticmethod
    def update(product):
        db.session.commit()
