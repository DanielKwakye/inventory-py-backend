from patterns.commands.command import Command
from patterns.proxys.inventory_proxy import InventoryProxy


class GetProductsCommand(Command):

    def __init__(self, inventory_proxy: InventoryProxy, category ="shoes"):
        self.inventory_proxy = inventory_proxy
        self.category = category


    def execute(self):
        return self.inventory_proxy.get_products(self.category)
