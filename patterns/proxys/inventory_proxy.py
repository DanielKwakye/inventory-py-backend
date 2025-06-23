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
            product.save()
            self._inventory.add_stock(product, quantity)
            return {"success": True}
        else:
            self.notify_observers("create_product_permission_denied")
            return {"success": False, "error": "Permission denied to create product."}

    def add_stock(self, product: Product, quantity: int):
        if self.has_permission("add_stock"):
            self._inventory.add_stock(product, quantity)
        else:
            self.notify_observers("add_stock_permission_denied")

    def reduce_stock(self, product: Product, quantity: int):
        if self.has_permission("reduce_stock"):
            self._inventory.reduce_stock(product, quantity)
        else:
            self.notify_observers("reduce_stock_permission_denied")

    def has_permission(self, action: str) -> bool:
        if not self.role:
            return False

        # Define roles allowed to perform actions
        if action in ["add_stock", "reduce_stock", "create_product"] and self.role == "admin":
            return True

        return False