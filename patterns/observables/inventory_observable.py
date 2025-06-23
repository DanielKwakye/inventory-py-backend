from models.product_model import Product
from models.stock_model import Stock
from patterns.observables.observable import Observable

class Inventory(Observable):
    def __init__(self):
        super().__init__()

    def add_stock(self, product: Product, quantity: int):
        stock = Stock(product.id, quantity)
        stock.save()
        self.notify_observers(f"Stock added: {product.title} x{quantity}")

    def reduce_stock(self, product: Product, quantity: int):
        stock = Stock(product.id, quantity)
        stock.save()
        self.notify_observers(f"Stock reduced: {product.title} x{quantity}")
        # success = stock.reduce(quantity)
        # if success:
        #
        # else:
        #     self.notify_observers(f"Insufficient stock to reduce: {product.title}")


