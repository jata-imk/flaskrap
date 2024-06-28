from datetime import datetime
from app import db


class ProductInventory(db.Model):
    __tablename__ = "product_inventory"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    linked_product_id = db.Column(
        db.Integer, db.ForeignKey("product.id"), nullable=False
    )
    linked_vendor_id = db.Column(db.Integer, db.ForeignKey("vendor.id"), nullable=False)
    sku = db.Column(db.String(63), nullable=False, default="", server_default="")
    price = db.Column(
        db.Numeric(precision=15, scale=5), nullable=False, default=0.0, server_default="0"
    )
    quantity = db.Column(db.Integer, nullable=False, default=0, server_default="0")
    created_at = db.Column(
        db.DateTime, default=datetime.now, server_default="CURRENT_TIMESTAMP()"
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now,
        server_default="CURRENT_TIMESTAMP()",
        onupdate=datetime.now,
    )

    product = db.relationship("Product", backref=db.backref("inventories", lazy=True))
    vendor = db.relationship("Vendor", backref=db.backref("inventories", lazy=True))

    def __repr__(self):
        return f"<ProductInventory {self.id} - Product: {self.linked_product_id}, Vendor: {self.linked_vendor_id}>"
