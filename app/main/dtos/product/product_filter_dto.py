class ProductFilter:
    def __init__(self, name=None, category_id=None, limit=None, include=None):
        self.name = name
        self.category_id = category_id
        self.limit = limit
        self.include = include
