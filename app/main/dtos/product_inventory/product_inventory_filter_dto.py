from ctypes import Array


class ProductInventoryFilter:
    def __init__(self, products_id:Array=None, vendor_id=None, price=None, limit=None, include:dict=None):
        self.products_id = products_id
        self.vendor_id = vendor_id
        self.price = price
        self.limit = limit
        self.include = include
