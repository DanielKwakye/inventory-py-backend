from models.product_model import Product
from patterns.commands.command import Command
from patterns.proxys.inventory_proxy import InventoryProxy


class UpdateStockCommand(Command):

    def __init__(self, inventory_proxy: InventoryProxy, product_id:int, new_quantity: int):
        self.inventory_proxy = inventory_proxy
        self.product_id = product_id
        self.new_quantity = new_quantity

    def execute(self):
        return self.inventory_proxy.update_stock(product_id=self.product_id, quantity=self.new_quantity)