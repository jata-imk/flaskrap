from datetime import datetime
from app import db


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(127), nullable=False, default="", server_default="")
    description = db.Column(
        db.String(255), nullable=False, default="", server_default=""
    )
    sku = db.Column(db.String(63), nullable=False, unique=True)
    small_image = db.Column(
        db.String(127), nullable=False, default="", server_default=""
    )
    out_of_stock = db.Column(
        db.Boolean, nullable=False, default=True, server_default="1"
    )  # Por defecto es como si estuviera fuera de stock
    categories_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey("brand.id"), nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.now, server_default="CURRENT_TIMESTAMP()"
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now,
        server_default="CURRENT_TIMESTAMP()",
        onupdate=datetime.now,
    )

    category = db.relationship("Category", backref=db.backref("products", lazy=True))
    brand = db.relationship("Brand", backref=db.backref("products", lazy=True))
    images = db.relationship("Image", secondary="product_image", backref="products")
    inventories = db.relationship(
        "ProductInventory", back_populates="product", lazy=True
    )
    prompt_history = db.relationship(
        "PromptHistory", back_populates="product", lazy=True
    )

    def __repr__(self):
        return f"<Product {self.name}>"

    def as_dict(self):
        product_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}

        if "inventories" in self.__dict__:
            product_dict["inventories"] = [
                inventory.as_dict() for inventory in self.inventories
            ]

        return product_dict
