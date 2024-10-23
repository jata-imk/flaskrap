class ProductFilter:
    def __init__(self, id:int=None, name:str=None, category_id:int=None, page:int=None, page_size:int=None, include:dict=None):
        self.id = id
        self.name = name
        self.category_id = category_id
        self.page = page
        self.page_size = page_size
        self.include = include
