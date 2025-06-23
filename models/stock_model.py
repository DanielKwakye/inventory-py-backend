from models.base_model import BaseModel
from patterns.singletons.database_singleton import DatabaseConnection


class Stock(BaseModel):
    def __init__(self, product_id: int, quantity: int):
        self.product_id = product_id
        self.quantity = quantity

    def save(self):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS stock (id INTEGER PRIMARY KEY AUTOINCREMENT,product_id INTEGER,quantity INTEGER,FOREIGN KEY(product_id) REFERENCES products(id))")

        cursor.execute("SELECT quantity FROM stock WHERE product_id = ?", (self.product_id,))
        row = cursor.fetchone()

        if row:
            new_qty = row[0] + self.quantity
            cursor.execute("UPDATE stock SET quantity = ? WHERE product_id = ?", (new_qty, self.product_id))
        else:
            cursor.execute("INSERT INTO stock (product_id, quantity) VALUES (?, ?)", (self.product_id, self.quantity))

        conn.commit()

    # def reduce(self):
    #     conn = DatabaseConnection().get_connection()
    #     cursor = conn.cursor()
    #
    #     cursor.execute("SELECT quantity FROM stock WHERE product_id = ?", (self.product_id,))
    #     row = cursor.fetchone()
    #
    #     if row and row[0] >= self.quantity:
    #         new_qty = row[0] - selectquantity
    #         cursor.execute("UPDATE stock SET quantity = ? WHERE product_id = ?", (new_qty, self.product_id))
    #         conn.commit()
    #         return True
    #     return False
