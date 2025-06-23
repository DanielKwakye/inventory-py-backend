from models.product_model import Product
from patterns.commands.command import Command
from patterns.proxys.inventory_proxy import InventoryProxy


class AddStockCommand(Command):

    def __init__(self, inventory_proxy: InventoryProxy, author_id:int, product_id: int, quantity: int):
        self.author_id = author_id
        self.inventory_proxy = inventory_proxy
        self.product_id = product_id
        self.quantity = quantity

    def execute(self):
        product = Product.find_by_id(self.product_id)
        self.inventory_proxy.add_stock(product=product, quantity=self.quantity)

    def undo(self):
        product = Product.find_by_id(self.product_id)
        self.inventory_proxy.reduce_stock(product=product, quantity=self.quantity)