# The factory method decides which subclass to instantiate.
from models.product_model import Product
from patterns.decorators.discouted_product import DiscountedProduct
from patterns.decorators.taxed_product import TaxedProduct

class ProductFactory:
    @staticmethod
    def new_product(title: str, category: str, cost_price: float, selling_price: float, image_path:str, tax_value:float = 0, discount_perc: float = 0) -> Product:

        product = Product(
            title=title,
            category=category,
            cost_price=cost_price,
            selling_price=selling_price,
            image_path=image_path
        )

        # Apply decorators based on category

        if tax_value != 0 and discount_perc != 0:
            product.tax_value = tax_value
            product.discount_perc = discount_perc
        else:
            if tax_value != 0:
                product = TaxedProduct(product, tax_value)

            if discount_perc != 0:
                product = DiscountedProduct(product, discount_perc)

        return product

