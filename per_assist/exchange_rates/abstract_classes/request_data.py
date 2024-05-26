from abc import ABC, abstractmethod

class Request_data(ABC):

    @abstractmethod
    async def get_data(self, source):
        pass