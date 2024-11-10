from datetime import datetime
from app import db


class Brand(db.Model):
    __tablename__ = "brand"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(
        db.DateTime, default=datetime.now, server_default="CURRENT_TIMESTAMP()"
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now,
        server_default="CURRENT_TIMESTAMP()",
        onupdate=datetime.now,
    )

    images = db.relationship("Image", secondary="brand_image", backref="brands")

    def __repr__(self):
        return f"<Brand {self.name}>"
