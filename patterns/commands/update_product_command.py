from patterns.commands.command import Command
from patterns.proxys.inventory_proxy import InventoryProxy


class EditProductCommand(Command):

    def __init__(self, inventory_proxy: InventoryProxy, product_id: int, title, cost_price, selling_price, tax_value, discount_perc):
        self.inventory_proxy = inventory_proxy
        self.product_id = product_id
        self.title = title
        self.cost_price = cost_price
        self.selling_price = selling_price,
        self.tax_value = tax_value
        self.discount_perc = discount_perc

    def execute(self):
        return self.inventory_proxy.update_product(
            product_id=self.product_id,
            title=self.title,
            cost_price=self.cost_price,
            selling_price=self.selling_price,
            tax_value=self.tax_value,
            discount_perc=self.discount_perc
        )