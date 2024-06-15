from app import db
from app.main.models import Vendor

class VendorRepository:
    @staticmethod
    def get_by_name(name):
        return db.session.query(Vendor).filter_by(name=name).first()

    @staticmethod
    def create(vendor):
        db.session.add(vendor)
        db.session.commit()

    @staticmethod
    def update(vendor):
        db.session.commit()
