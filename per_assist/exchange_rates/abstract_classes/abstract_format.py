from abc import ABC, abstractmethod
# from classes.Request_rates import Request_rates

class Abstract_format(ABC):
    # def __init__(self, rates: Request_rates) -> None:
    #     self.rates = rates

    @abstractmethod
    def generate(self, count = None):
        pass


