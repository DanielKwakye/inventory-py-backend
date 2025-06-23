# The Strategy Pattern lets you define a family of algorithms, put each one in a separate class, and make them interchangeable at runtime.
from abc import ABC, abstractmethod

class ProductStrategy(ABC):

    @abstractmethod
    def calculate_price(self, actual_price: float):
        raise NotImplemented


