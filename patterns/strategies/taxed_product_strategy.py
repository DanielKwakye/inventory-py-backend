from patterns.strategies.product_strategy import ProductStrategy

class TaxedProductStrategy(ProductStrategy):

    def calculate_price(self, actual_price: float):
        pass