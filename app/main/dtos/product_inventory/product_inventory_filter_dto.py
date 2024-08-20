class ProductInventoryFilter:
    def __init__(self, product_id=None, vendor_id=None, price=None, limit=None):
        self.product_id = product_id
        self.vendor_id = vendor_id
        self.price = price
        self.limit = limit
