from app import db
from app.main.models.PromptHistory import PromptHistory

from sqlalchemy import and_, func


class PromptHistoryRepository:
    @staticmethod
    def create(prompt_history: PromptHistory):
        db.session.add(prompt_history)
        db.session.commit()

    @staticmethod
    def get_by_product_id(product_id):
        return db.session.query(PromptHistory).filter_by(product_id=product_id).all()

    @staticmethod
    def get_by_product_id_and_created_at(product_id, created_at):
        conditions = and_(
            func.date(PromptHistory.created_at) == created_at,
            PromptHistory.product_id == product_id
        )
        return (
            db.session.query(PromptHistory)
            .filter(conditions)
            .first()
        )
