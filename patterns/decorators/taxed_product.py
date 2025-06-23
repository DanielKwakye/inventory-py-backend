from patterns.decorators.product_decorator import ProductDecorator


class TaxedProduct(ProductDecorator):
    def __init__(self, product, tax_value):
        super().__init__(product)
        self.tax_value = tax_value

    def get_price(self):
        return self.get_price() + self.tax_value