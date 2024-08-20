from app import db
from app.main.models.ProductInventory import ProductInventory


class ProductInventoryRepository:
    @staticmethod
    def get_all(filter):
        query = ProductInventory.query

        if filter.product_id:
            if isinstance(filter.product_id, list):
                query = query.filter(
                    ProductInventory.linked_product_id.in_(filter.product_id)
                )
            else:
                query = query.filter(
                    ProductInventory.linked_product_id == filter.product_id
                )

        if filter.vendor_id:
            query = query.filter(ProductInventory.linked_vendor_id == filter.vendor_id)

        if filter.price:
            query = query.filter(ProductInventory.price == filter.price)

        if filter.limit:
            query = query.limit(filter.limit)

        query = query.order_by(ProductInventory.id.asc())

        return query.all()

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
