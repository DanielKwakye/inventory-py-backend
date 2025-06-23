# Decorator Pattern: This is a structural pattern that helps attach additional responsibilities to an
# object dynamically. Decorators provide a flexible alternative to subclassing for extending
# functionality. We selected this design pattern to be used to create additional functionality for the
# product object, such as discount calculations or tax calculations.

from models.product_model import Product

class ProductDecorator(Product):
    def __init__(self, product):
        super().__init__(product.title, product.category, product.cost_price, product.selling_price, product.image_path)

    def get_price(self):
        return self.get_price()

    def __str__(self):
        return self.__str__()


