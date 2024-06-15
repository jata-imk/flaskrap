from app import db
from app.main.models import Brand

class BrandRepository:
    @staticmethod
    def get_by_name(name):
        return db.session.query(Brand).filter_by(name=name).first()

    @staticmethod
    def create(brand):
        db.session.add(brand)
        db.session.commit()

    @staticmethod
    def update(brand):
        db.session.commit()
