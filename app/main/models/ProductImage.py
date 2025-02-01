from app import db


class ProductImage(db.Model):
    __tablename__ = "product_image"

    product_id = db.Column(
        db.Integer, db.ForeignKey("product.id", ondelete="CASCADE"), primary_key=True
    )
    image_id = db.Column(
        db.Integer, db.ForeignKey("image.id", ondelete="CASCADE"), primary_key=True
    )
    is_primary = db.Column(db.Boolean, nullable=False,default=False, server_default="0")
