from app import db


class CategoryImage(db.Model):
    __tablename__ = "category_image"

    category_id = db.Column(
        db.Integer, db.ForeignKey("category.id", ondelete="CASCADE"), primary_key=True
    )
    image_id = db.Column(
        db.Integer, db.ForeignKey("image.id", ondelete="CASCADE"), primary_key=True
    )
    is_primary = db.Column(db.Boolean, default=False, nullable=False)
