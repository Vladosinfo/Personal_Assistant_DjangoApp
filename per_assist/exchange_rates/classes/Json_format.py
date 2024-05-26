from ..abstract_classes.abstract_format import Abstract_format
# from .Request_rates import Request_rates
# from ..abstract_classes.request_data import Request_data

class Json_format(Abstract_format):
   
    # def __init__(self, rates: Request_data, source) -> None:
    #     self.rates = rates
    #     self.source = source

    def __init__(self, data) -> None:
        self.data = data

    
    def generate(self):
        dict = {self.data["date"] : {}}
        for item in self.data["exchangeRate"]:
            if item["currency"] == "EUR" or item["currency"] == "USD" or item["currency"] == "GBP":
                edict = {item["currency"] : {"sale" : round(float(item["saleRate"]), 1),                       
                                             "purchase" : round(float(item["purchaseRate"]), 2)}
                         }
                dict[self.data["date"]].update(edict)
        return dict

