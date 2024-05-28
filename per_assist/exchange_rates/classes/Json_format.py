from ..abstract_classes.abstract_format import Abstract_format

class Json_format(Abstract_format):

    def __init__(self, data) -> None:
        self.data = data

    
    def generate(self):
        dict_rates = {}
        split_data = self.data["date"].split('.')
        data = split_data[2] + '-' + split_data[1] + '-' + split_data[0]
        dict_rates["date"] = data  #.strftime("%Y.%d.%m")
        dict_rates["baseCurrency"] = self.data["baseCurrencyLit"]
        dict_rates["exchangeRateList"] = []
        for item in self.data["exchangeRate"]:
            # CHF - Swiss Franc
            # GBP - Pound sterling
            if item["currency"] == "EUR" or item["currency"] == "USD" or item["currency"] == "GBP" or item["currency"]  == "PLN" or item["currency"] == "CHF":
                dict_currency = {}
                dict_currency["currency"] = item["currency"]
                dict_currency["saleRate"] = f"{float(item['saleRate']):.2f}"
                dict_currency["purchaseRate"] = f"{float(item['purchaseRate']):.2f}"
                dict_rates["exchangeRateList"].append(dict_currency)
        return dict_rates
