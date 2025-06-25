from patterns.commands.command import Command
from patterns.proxys.inventory_proxy import InventoryProxy


class CheckoutCommand(Command):

    def __init__(self, inventory_proxy: InventoryProxy, payload: list[dict[str, int]]):
        self.inventory_proxy = inventory_proxy
        self.payload = payload

    def execute(self):
        return self.inventory_proxy.checkout(payload=self.payload)
