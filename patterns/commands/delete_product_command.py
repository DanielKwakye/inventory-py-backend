from models.product_model import Product
from patterns.commands.command import Command
from patterns.proxys.inventory_proxy import InventoryProxy


class DeleteProductCommand(Command):

    def __init__(self, inventory_proxy: InventoryProxy, product_id: int):
        self.inventory_proxy = inventory_proxy
        self.product_id = product_id

    def execute(self):
        return self.inventory_proxy.delete_product(product_id=self.product_id)
