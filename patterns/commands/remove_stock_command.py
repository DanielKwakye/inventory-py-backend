from models.product_model import Product
from patterns.commands.command import Command
from patterns.observables.inventory_observable import Inventory

class RemoveStockCommand(Command):

    def __init__(self, inventory: Inventory, product_id: int, quantity: int):
        self.inventory = inventory
        self.product_id = product_id
        self.quantity = quantity

    def execute(self):
        product = Product.find_by_id(self.product_id)
        self.inventory.reduce_stock(product=product, quantity=self.quantity)

    def undo(self):
        product = Product.find_by_id(self.product_id)
        self.inventory.add_stock(product=product, quantity=self.quantity)