from patterns.factories.product_factory import ProductFactory
from patterns.proxys.inventory_proxy import InventoryProxy
from patterns.commands.command import Command


class AddProductCommand(Command):

    def __init__(self, inventory: InventoryProxy, title: str, category: str,
                 cost_price: float, selling_price: float, quantity: int, image_path: str, tax_value: float, discount_perc: float):
        self.inventory = inventory
        self.title = title
        self.category = category
        self.cost_price = cost_price
        self.selling_price = selling_price
        self.quantity = quantity
        self.image_path = image_path
        self.tax_value = tax_value
        self.discount_perc = discount_perc

    def execute(self) -> dict:
        # Use factory to create the appropriate Product (may be decorated)
        product = ProductFactory.new_product(
            title=self.title,
            category=self.category,
            cost_price=self.cost_price,
            selling_price=self.selling_price,
            image_path=self.image_path,
            tax_value=self.tax_value,
            discount_perc=self.discount_perc
        )

        # Use proxy to attempt to create the product in inventory
        result = self.inventory.create_product(product, self.quantity)

        # Return the proxy's result (either success or permission denied)
        return result