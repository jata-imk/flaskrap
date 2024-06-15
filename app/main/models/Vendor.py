from datetime import datetime
from app import db


class Vendor(db.Model):
    __tablename__ = "vendor"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, default="", server_default="")
    created_at = db.Column(
        db.DateTime, default=datetime.now, server_default="CURRENT_TIMESTAMP()"
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now,
        server_default="CURRENT_TIMESTAMP()",
        onupdate=datetime.now,
    )

    def __repr__(self):
        return f"<Vendor {self.name}>"
