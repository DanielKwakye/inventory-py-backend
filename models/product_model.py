# # Decorator Pattern. Use it when:
# # You want to extend the functionality of an object without modifying its original class.
# # You want to keep your code open to extension but closed to modification (SOLID principle).
from models.base_model import BaseModel
from patterns.singletons.database_singleton import DatabaseConnection
from patterns.strategies.product_strategy import ProductStrategy

class Product(BaseModel):

    strategy: ProductStrategy = None
    discount_perc:float = 0
    tax_value:float = 0

    def __init__(self, title: str, category: str, cost_price: float, selling_price: float, image_path: str):
        self.title = title
        self.category = category
        self.cost_price = cost_price
        self.selling_price = selling_price
        self.image_path = image_path
        self.id = None

    def save(self) :
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT,category TEXT,cost_price REAL,selling_price REAL, image_path TEXT, tax_value REAL, discount_perc REAL)")

        # Insert product
        cursor.execute("INSERT INTO products (title, category, cost_price, selling_price, image_path, tax_value, discount_perc)VALUES (?, ?, ?, ?, ?, ?, ?)", (self.title, self.category, self.cost_price, self.selling_price, self.image_path, self.tax_value, self.discount_perc))
        conn.commit()
        self.id = cursor.lastrowid

    def get_price(self):
        if self.strategy:
            return self.strategy.calculate_price(self.selling_price)
        return self.selling_price

    def __str__(self):
        return f"{self.title} ({self.category}): ${self.get_price():.2f}"


# from models.base_model import BaseModel
# from patterns.strategies.product_strategy import ProductStrategy
#
#
# class Product(BaseModel):
#
#     strategy: ProductStrategy = None
#
#     def __init__(self, name: str, price: float):
#         self.name = name
#         self.price = price
#
#     @staticmethod
#     def find_all():
#         pass
#
#     @staticmethod
#     def find_by_id(table_id: int):
#         pass
#
#     def save(self):
#
#         pass
#
#     def set_strategy(self, strategy: ProductStrategy):
#         self.strategy = strategy
#         pass
#
#     def get_price(self):
#         if self.strategy is not None:
#             return self.strategy.calculate_price(self.price)
#         return self.price
#
#     def __str__(self):
#         return f"{self.name}: ${self.get_price():.2f}"
#
#
#
#
#
