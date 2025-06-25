# Proxy Pattern for Access Control
from models.product_model import Product
from patterns.observables.inventory_observable import Inventory
from patterns.observables.observable import Observer, Observable


class InventoryProxy(Observable):

    def __init__(self, inventory: Inventory):
        super().__init__()
        self._inventory = inventory
        self.role:str = None  # Set by controller (e.g., inventory_proxy.author = User(...))

    def create_product(self, product: Product, quantity: int) -> dict:
        if self.has_permission("create_product"):
            self._inventory.save_product(product=product)
            self._inventory.update_stock(product.id, quantity)
            return {"success": True}
        else:
            self.notify_observers("create_product_permission_denied")
            return {"success": False, "error": "Permission denied to create product."}

    def get_products(self, category: str):
        if self.has_permission("get_products_stock"):
            data = self._inventory.get_products_stocks(category=category)
            return { "success": True, "data": data }
        else:
            self.notify_observers("get_products_stock_permission_denied")
            return {"success": False, "error": "Permission denied to get products."}

    def update_stock(self, product_id: int, quantity: int):
        if self.has_permission("update_stock"):
            self._inventory.update_stock(product_id, quantity)
            return {"success": True}
        else:
            self.notify_observers("update_stock_permission_denied")
            return {"success": False, "error": "Permission denied"}

    def update_product(self, product_id, title: str, cost_price: float, selling_price: float, tax_value: float, discount_perc: float):
        if self.has_permission("update_product"):
            self._inventory.update_product(
                product_id, title, cost_price, selling_price, tax_value, discount_perc
            )
            return {"success": True}
        else:
            self.notify_observers("update_product_permission_denied")
            return {"success": False, "error": "Permission denied"}

    def delete_product(self, product_id: int):
        if self.has_permission("delete_product"):
            self._inventory.delete_product(product_id=product_id)
        else:
            self.notify_observers("delete_product_permission_denied")

    def checkout(self, payload: list[dict[str, int]]):
        if self.has_permission("checkout"):
            self._inventory.checkout(payload=payload)
        else:
            self.notify_observers("checkout_permission_denied")

    def has_permission(self, action: str) -> bool:

        # Both admin and customer can get products with their stocks
        if action in ["get_products_stock", "checkout"]:
            return True

        if not self.role:
            return False

        # Define roles allowed to perform actions
        if action in ["update_stock", "checkout", "update_product", "delete_product", "create_product", ] and self.role == "admin":
            return True

        return False