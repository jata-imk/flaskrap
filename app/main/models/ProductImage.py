from app import db

class ProductImage(db.Model):
    __tablename__ = "product_image"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False, nullable=False)

    product = db.relationship("Product", backref=db.backref("images", lazy=True))
