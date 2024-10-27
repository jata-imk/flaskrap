import copy

from app import db
from app.main.dtos.product.product_filter_dto import ProductFilter
from app.main.models.Product import Product
from app.main.models.ProductInventory import ProductInventory
from app.main.models.ProductIOHistory import ProductIOHistory

from app.main.repositories.product_io_history_repository import (
    ProductIOHistoryRepository,
)
from sqlalchemy import select, func
from sqlalchemy.orm import contains_eager


class ProductRepository:
    @staticmethod
    def get_principal_stmt(filter: ProductFilter):
        stmt = select(Product)
        
        if filter.id:
            stmt = stmt.where(Product.id == filter.id)

        if filter.name:
            stmt = stmt.where(Product.name.ilike(f"%{filter.name}%"))

        if filter.category_id:
            stmt = stmt.where(Product.category_id == filter.category_id)

        if filter.page and filter.page_size:
            offset = (filter.page - 1) * filter.page_size
            limit = filter.page_size

            subquery = (
                select(Product)
                .where(Product.name.ilike(f"%{filter.name}%") if filter.name else True)
                .offset(offset)
                .limit(limit)
                .with_only_columns(Product.id)
                .subquery()
            )
            
            stmt = stmt.join(subquery, Product.id == subquery.c.id)

        if filter.include:
            if "inventories" in filter.include:
                stmt = stmt.join(Product.inventories).options(
                    contains_eager(Product.inventories)
                )

                if (
                    filter.include["inventories"].include
                    and "io_history" in filter.include["inventories"].include
                ):
                    io_history_condition = (
                        ProductIOHistoryRepository.get_io_history_conditions(
                            filter.include["inventories"].include["io_history"]
                        )
                    )

                    stmt = stmt.join(
                        ProductIOHistory,
                        onclause=(ProductInventory.id == ProductIOHistory.inventory_id)
                        & io_history_condition,
                        isouter=True,
                    ).options(
                        contains_eager(Product.inventories).contains_eager(
                            ProductInventory.io_history
                        )
                    )

        return stmt

    @staticmethod
    # get the total count of products
    def get_count(filter: ProductFilter):
        filter_copy = copy.copy(filter)

        filter_copy.page = None
        filter_copy.page_size = None

        stmt = ProductRepository.get_principal_stmt(filter_copy)
        stmt = stmt.group_by(Product.id)

        stmt_subquery = stmt.subquery()

        stmt = select(func.count(stmt_subquery.c.id)).select_from(stmt_subquery)

        return db.session.execute(stmt).scalar()

    @staticmethod
    def get_all(filter):
        stmt = ProductRepository.get_principal_stmt(filter)

        stmt = stmt.group_by(Product.id)
        if filter.include:
            if "inventories" in filter.include:
                stmt = stmt.group_by(ProductInventory.id)
                if (
                    filter.include["inventories"].include
                    and "io_history" in filter.include["inventories"].include
                ):
                    stmt = stmt.group_by(ProductIOHistory.id)

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
