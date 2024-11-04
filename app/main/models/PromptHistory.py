from datetime import datetime

from app import db


class PromptHistory(db.Model):
    __tablename__ = "prompt_history"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prompt = db.Column(db.Text(), nullable=True)
    response = db.Column(db.Text(), nullable=True)
    api = db.Column(db.String(255), nullable=False, default="", server_default="")

    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=True)
    created_at = db.Column(
        db.DateTime, default=datetime.now, server_default="current_timestamp"
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.now,
        server_default="current_timestamp",
        onupdate=datetime.now,
    )

    # unique index for product_id and created_at
    __table_args__ = (db.UniqueConstraint("product_id", "created_at"), {})

    product = db.relationship("Product", back_populates="prompt_history", lazy=True)

    def __repr__(self):
        return f"<PromptHistory {self.display_text}>"

    def as_dict(self):
        prompt_history_dict = {
            c.name: getattr(self, c.name) for c in self.__table__.columns
        }

        return prompt_history_dict
