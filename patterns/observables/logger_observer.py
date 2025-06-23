# Observer to print logs
from patterns.observables.observable import Observer

class LoggerObserver(Observer):
    def update(self, message):
        print("custom_log=", message)