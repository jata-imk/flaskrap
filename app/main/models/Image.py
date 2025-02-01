from datetime import datetime
from app import db


class Image(db.Model):
    __tablename__ = "image"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    src = db.Column(db.String(255), nullable=False)
    type = db.Column(
        db.Enum("archivo", "url", name="tipo"), nullable=False, default="archivo"
    )
    name = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255), nullable=False, default="", server_default="")
    created_at = db.Column(
        db.DateTime, default=datetime.now, server_default="CURRENT_TIMESTAMP()"
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now,
        server_default="CURRENT_TIMESTAMP()",
        onupdate=datetime.now,
    )

    def as_dict(self):
        self_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}

        return self_dict
