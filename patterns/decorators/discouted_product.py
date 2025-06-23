from models.product_model import Product
from patterns.decorators.product_decorator import ProductDecorator


class DiscountedProduct(ProductDecorator):
    def __init__(self, product: Product, discount_perc: float):
        super().__init__(product)
        self.discount_perc = discount_perc

    def get_price(self):
        return self.get_price() - (self.get_price() * self.discount_perc)
