from abc import ABC, abstractmethod

class Abstract_format(ABC):

    @abstractmethod
    def generate(self, count = None):
        pass
