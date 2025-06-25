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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                category TEXT,
                cost_price REAL,
                selling_price REAL,
                image_path TEXT,
                tax_value REAL,
                discount_perc REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Insert product
        cursor.execute("""
            INSERT INTO products (title, category, cost_price, selling_price, image_path, tax_value, discount_perc)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            self.title,
            self.category,
            self.cost_price,
            self.selling_price,
            self.image_path,
            self.tax_value,
            self.discount_perc
        ))
        conn.commit()
        self.id = cursor.lastrowid

    @staticmethod
    def find_all(category: str):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT 
        products.id,
        products.title,
        products.category,
        products.cost_price,
        products.selling_price,
        stocks.quantity,
        products.created_at, 
        products.image_path,
        products.tax_value,
        products.discount_perc
         FROM products JOIN stocks ON products.id = stocks.product_id WHERE products.category = ?""",(category,))

        # Convert to list of dicts
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.commit()

        return results

    def get_price(self):
        if self.strategy:
            return self.strategy.calculate_price(self.selling_price)
        return self.selling_price

    @staticmethod
    def delete(product_id: int):
        conn = DatabaseConnection().get_connection()
        conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()


    def update(self, title: str, cost_price: float, selling_price: float, tax_value: float, discount_perc: float):
        conn = DatabaseConnection().get_connection()
        conn.execute(
            """
            UPDATE products
            SET title = ?,
                cost_price = ?,
                selling_price = ?,
                tax_value = ?,
                discount_perc = ?
            WHERE id = ?
            """,
            (title, cost_price, selling_price, tax_value, discount_perc, self.id)
        )
        conn.commit()

    @staticmethod
    def find_by_id(table_id: int):
        conn = DatabaseConnection().get_connection()
        cursor = conn.execute("SELECT * FROM products WHERE id = ?", (table_id,))
        row = cursor.fetchone()
        if row:
            # row = (id, title, category, cost_price, selling_price, image_path, tax_value, discount_perc, created_at)
            _, title, category, cost_price, selling_price, image_path, tax_value, discount_perc, _ = row

            product = Product(title, category, cost_price, selling_price, image_path)
            product.id = table_id
            product.tax_value = tax_value
            product.discount_perc = discount_perc
            return product
        return None


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
