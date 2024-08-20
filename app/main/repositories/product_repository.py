from app import db
from app.main.models.Product import Product
from app.main.models.ProductInventory import ProductInventory
from app.main.models.ProductIOHistory import ProductIOHistory

from sqlalchemy import select, func, and_
from sqlalchemy.orm import aliased, contains_eager


class ProductRepository:
    @staticmethod
    def get_all(filter):
        stmt = select(Product)

        if filter.name:
            stmt = stmt.where(Product.name.ilike(f"%{filter.name}%"))

        if filter.category_id:
            stmt = stmt.where(Product.category_id == filter.category_id)

        if filter.limit:
            stmt = stmt.limit(filter.limit)

        if filter.include:
            filter.include = filter.include.split(",")

            if "inventories" in filter.include:
                stmt = stmt.join(Product.inventories).options(
                    contains_eager(Product.inventories)
                )

                if "io_history" in filter.include:
                    # Subquery para obtener los últimos 7 registros
                    subquery = select(
                        ProductIOHistory,
                        func.row_number()
                        .over(
                            partition_by=ProductIOHistory.inventory_id,
                            order_by=ProductIOHistory.transaction_date.desc(),
                        )
                        .label("row_num"),
                    ).subquery()

                    filtered_io_history = aliased(ProductIOHistory, subquery)

                    stmt = stmt.join(
                        filtered_io_history,
                        onclause=and_(
                            ProductInventory.id == filtered_io_history.inventory_id,
                            subquery.c.row_num <= 21,
                        ),
                        isouter=True,
                    ).options(
                        contains_eager(Product.inventories).contains_eager(
                            ProductInventory.io_history, alias=filtered_io_history
                        )
                    )

        stmt = stmt.order_by(Product.id.asc())

        return db.session.execute(stmt).unique().scalars().all()

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
