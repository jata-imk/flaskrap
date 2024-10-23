from ctypes import Array


class ProductInventoryFilter:
    def __init__(self, products_id:Array=None, vendor_id=None, price=None, page:int=None, page_size:int=None, include:dict=None):
        self.products_id = products_id
        self.vendor_id = vendor_id
        self.price = price
        self.page = page
        self.page_size = page_size
        self.include = include
