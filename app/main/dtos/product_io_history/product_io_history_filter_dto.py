class ProductIOHistoryFilter:
    def __init__(self, inventory_id=None, start_date=None, end_date=None, page:int=None, page_size:int=None):
        self.inventory_id = inventory_id
        self.start_date = start_date
        self.end_date = end_date
        self.page = page
        self.page_size = page_size
