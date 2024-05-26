import aiohttp
from ..abstract_classes.request_data import Request_data

class Request_rates(Request_data):
    async def get_data(self, source):
        async with aiohttp.ClientSession() as session:
            # async with session.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5') as response:
            # async with session.get('https://api.privatbank.ua/p24api/exchange_rates?date=24.02.2024') as response:
            async with session.get(source) as response:
                result = await response.json()
                return result
            