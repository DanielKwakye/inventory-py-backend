from abc import ABC, abstractmethod

class BaseModel(ABC):
    id: int = None
    # @staticmethod
    # @abstractmethod
    # def find_all():
    #     pass
    #
    # @staticmethod
    # @abstractmethod
    # def find_by_id(table_id: int):
    #     pass

    @abstractmethod
    def save(self):
        pass