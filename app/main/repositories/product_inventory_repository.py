from app import db
from app.main.models.ProductInventory import ProductInventory

from sqlalchemy import select


class ProductInventoryRepository:
    @staticmethod
    def get_all(filter):
        stmt = select(ProductInventory)

        if filter.product_id:
            if isinstance(filter.product_id, list) is False:
                filter.product_id = [filter.product_id]

            stmt = stmt.where(
                ProductInventory.linked_product_id.in_(filter.product_id)
            )

        if filter.vendor_id:
            stmt = stmt.where(ProductInventory.linked_vendor_id == filter.vendor_id)

        if filter.price:
            stmt = stmt.where(ProductInventory.price == filter.price)

        if filter.limit:
            stmt = stmt.limit(filter.limit)

        stmt = stmt.order_by(ProductInventory.id.asc())

        return db.session.execute(stmt).unique().scalars().all()

    @staticmethod
    def get_by_product_id(id):
        return (
            db.session.query(ProductInventory).filter_by(linked_product_id=id).first()
        )

    @staticmethod
    def create(product_inventory):
        db.session.add(product_inventory)
        db.session.commit()

    @staticmethod
    def update(product_inventory):
        db.session.commit()
