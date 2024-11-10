from app import db


class BrandImage(db.Model):
    __tablename__ = "brand_image"

    brand_id = db.Column(
        db.Integer, db.ForeignKey("brand.id", ondelete="CASCADE"), primary_key=True
    )
    image_id = db.Column(
        db.Integer, db.ForeignKey("image.id", ondelete="CASCADE"), primary_key=True
    )
    is_primary = db.Column(db.Boolean, default=False, nullable=False)
