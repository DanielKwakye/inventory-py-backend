from models.product_model import Product
from models.stock_model import Stock
from patterns.observables.observable import Observable
from patterns.strategies.created_at_sort_strategy import CreatedAtSortStrategy


class Inventory(Observable):
    def __init__(self):
        super().__init__()


    def get_products_stocks(self, category: str):
        products = Product.find_all(category)
        sort_strategy = CreatedAtSortStrategy()
        self.notify_observers(f"Products fetch successful")
        return sort_strategy.sort(products)


    def find_product_by_id(self, product_id: int):
        product = Product.find_by_id(table_id=product_id)
        self.notify_observers(f"Product returned: {product.title}")
        return product

    def find_stock_by_product_id(self, product_id: int):
        stock = Stock.find_by_product_id(product_id=product_id)
        self.notify_observers(f"Stock returned")
        return stock

    def save_product(self, product: Product):
        product.save()
        self.notify_observers(f"Product saved: {product.title}")

    def update_stock(self, product_id: int, quantity: int):
        stock = Stock(product_id, quantity)
        stock.save()
        self.notify_observers(f"Stock updated: pId:{product_id} x{quantity}")

    def delete_product(self, product_id: int):
        Product.delete(product_id=product_id)
        self.notify_observers(f"Product deleted:")

    def update_product(self, product_id, title: str, cost_price: float, selling_price: float, tax_value: float, discount_perc: float):
        product = self.find_product_by_id(product_id=product_id)
        if product is not None:
            product.update(
                title, cost_price, selling_price, tax_value, discount_perc
            )
        self.notify_observers(f"Stock updated: {product.title}")

    def checkout(self, payload: list[dict[str, int]]):
        for item in payload:
            product_id = item["product_id"]
            quantity = item["quantity"]
            product = self.find_product_by_id(product_id)
            stock = self.find_stock_by_product_id(product_id=product_id)
            if stock is not None:
                existing_qty = stock.quantity
                new_quantity = existing_qty - quantity
                if new_quantity < 5:
                    self.notify_observers(f"Stock values for this product has dropped below 5: {product.title}")
                if new_quantity < 0:
                    new_quantity = 0
                new_stock = Stock(product_id=product_id, quantity=new_quantity)
                new_stock.save()

        self.notify_observers(f"checkout completed")

