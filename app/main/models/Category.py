from app import db


class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    display_text = db.Column(db.String(63), nullable=False)
    description = db.Column(
        db.String(255), nullable=False, default="", server_default=""
    )
    parent_category_id = db.Column(
        db.Integer, db.ForeignKey("category.id"), nullable=True
    )

    parent_category = db.relationship(
        "Category", remote_side=[id], backref="subcategories"
    )
    images = db.relationship(
        "Image", secondary="category_image", backref="categories"
    )

    def __repr__(self):
        return f"<Category {self.display_text}>"
