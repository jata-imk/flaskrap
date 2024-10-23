from app import db
from app.main.dtos.product_io_history.product_io_history_filter_dto import (
    ProductIOHistoryFilter,
)
from app.main.models.ProductIOHistory import ProductIOHistory
from sqlalchemy import and_, func


class ProductIOHistoryRepository:
    @staticmethod
    def get_io_history_conditions(filters: ProductIOHistoryFilter):
        conditions = and_(
            func.date(ProductIOHistory.transaction_date) >= filters.start_date if filters.start_date else True,
            func.date(ProductIOHistory.transaction_date) <= filters.end_date if filters.end_date else True
        )
        return conditions

    @staticmethod
    def create(history):
        db.session.add(history)
        db.session.commit()

    @staticmethod
    def get_by_inventory_id(inventory_id):
        return (
            db.session.query(ProductIOHistory)
            .filter_by(inventory_id=inventory_id)
            .all()
        )
