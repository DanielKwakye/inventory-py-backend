# Command Pattern: This is another behavioral pattern that encapsulates a request as an object,
# allowing for parameterization of clients with different requests, queuing of requests, and logging
# of the requests. We selected the command pattern because we needed to handle user actions such
# as adding, editing, and deleting product operations.

from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError()

    # @abstractmethod
    # def undo(self):
    #     raise NotImplementedError()