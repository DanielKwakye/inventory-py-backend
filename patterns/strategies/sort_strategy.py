# The Strategy Pattern lets you define a family of algorithms, put each one in a separate class, and make them interchangeable at runtime.

from abc import ABC, abstractmethod

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list:
        pass