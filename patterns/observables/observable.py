# Observer Pattern: The users of the inventory need to be able to get notified when there has been a
# change or update on the system. The observer pattern is a type of behavioral pattern that define a
# one-to-many dependency between objects so that when one object changes state, all its
# dependents are notified and updated automatically. The pattern was chosen because we needed to
# add the notification functionality.

from abc import ABC, abstractmethod


# Observer classes receive updates
class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass


# Observable classes emits updates
class Observable:

    _observers: list[Observer] = []

    def __init__(self):
        self._observers = []

    def add_observer(self, observer: Observer):
        self._observers.append(observer)

    def notify_observers(self, event):
        for observer in self._observers:
            observer.update(event)


