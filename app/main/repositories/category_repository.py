from app import db
from app.main.models.Category import Category

class CategoryRepository:
    @staticmethod
    def get_by_display_text(display_text):
        return db.session.query(Category).filter_by(display_text=display_text).first()

    @staticmethod
    def create(category):
        db.session.add(category)
        db.session.commit()

    @staticmethod
    def get_or_create(display_text, parent_category=None):
        category = CategoryRepository.get_by_display_text(display_text)
        if not category:
            category = Category(display_text=display_text, parent_category=parent_category)
            CategoryRepository.create(category)
        return category
