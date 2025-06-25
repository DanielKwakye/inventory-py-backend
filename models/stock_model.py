from models.base_model import BaseModel
from patterns.singletons.database_singleton import DatabaseConnection


class Stock(BaseModel):
    def __init__(self, product_id: int, quantity: int):
        self.product_id = product_id
        self.quantity = quantity

    def save(self):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS stocks (id INTEGER PRIMARY KEY AUTOINCREMENT,product_id INTEGER,quantity INTEGER,FOREIGN KEY(product_id) REFERENCES products(id))")

        cursor.execute("SELECT quantity FROM stocks WHERE product_id = ?", (self.product_id,))
        row = cursor.fetchone()

        if row:
            new_qty = row[0] + self.quantity
            cursor.execute("UPDATE stocks SET quantity = ? WHERE product_id = ?", (new_qty, self.product_id))
        else:
            cursor.execute("INSERT INTO stocks (product_id, quantity) VALUES (?, ?)", (self.product_id, self.quantity))

        conn.commit()

    @staticmethod
    def delete_by_product_id(product_id:int):
        conn = DatabaseConnection().get_connection()
        conn.execute("DELETE FROM stocks WHERE product_id = ?", (product_id,))
        conn.commit()

    @staticmethod
    def find_by_product_id(product_id: int):
        conn = DatabaseConnection().get_connection()
        cursor = conn.execute("SELECT * FROM stocks WHERE product_id = ?", (product_id,))
        row = cursor.fetchone()
        conn.commit()
        if row:
            # row = (id, product_id, quantity)
            stock = Stock(product_id=row[1], quantity=row[2])
            stock.id = row[0]
            return stock
        return None
