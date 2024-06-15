from datetime import datetime
from app import db


class ProductIOHistory(db.Model):
    __tablename__ = "product_io_history"

    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey("product_inventory.id"), nullable=False)

    io_type = db.Column(
        db.Enum("IN", "OUT", "PRICE_UPDATE", name="io_type"),
        nullable=False,
        default="PRICE_UPDATE",
        server_default="PRICE_UPDATE",
    )  # Tipo de transacción

    quantity = db.Column(
        db.Integer, nullable=False, default=0, server_default="0"
    )  # Cantidad de productos en la transacción

    price = db.Column(
        db.Numeric(precision=15, scale=5),
        nullable=False,
        default=0.0,
        server_default="0",
    )  # Precio del producto en la transacción

    transaction_date = db.Column(
        db.DateTime,
        default=datetime.now,
        server_default="CURRENT_TIMESTAMP()",
        nullable=False,
    )  # Fecha de la transacción

    created_at = db.Column(
        db.DateTime, default=datetime.now, server_default="CURRENT_TIMESTAMP()"
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.now,
        server_default="CURRENT_TIMESTAMP()",
        onupdate=datetime.now(),
    )

    inventory = db.relationship(
        "ProductInventory", backref=db.backref("io_history", lazy=True)
    )

    def __repr__(self):
        return f"<IO History for product {self.inventory.linked_product_id} with vendor {self.inventory.linked_vendor_id}>"
