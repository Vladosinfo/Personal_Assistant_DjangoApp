from typing import Any
from ..abstract_classes.request_data import Request_data

class Client:
    def __init__(self, rates: Request_data, source):
        self.rates = rates
        self.source = source

    
    async def get_data(self):
        return await self.rates.get_data(self.rates, self.source)

