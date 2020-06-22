import requests
import pyotp
from game import Item
from datetime import datetime
import statistics

class BitskinsAPI:

    def __init__(self, config):
        self.api_endpoint = config["bitskins_reload"]["api_endpoint"]
        self.api_key = config["bitskins_reload"]["api_key"]
        self.price_calculation = config["bitskins_reload"]["price_calculation"]
        self.pricing_time_period = config["bitskins_reload"]["pricing_time_period"]
        self.exclude_extremes = config["bitskins_reload"]["exclude_extremes"]
        self.pricing_min_amount_sold = config["bitskins_reload"]["pricing_min_amount_sold"]
        self.token_generator = pyotp.TOTP(config["bitskins_reload"]["two_factor_secret"])

    def get_items(self, items):
        bitskins_items = []
        for item in items:
            if item.price != 0:
                bitskins_item = self.generate_item(item.name)
                bitskins_items.append(bitskins_item)
        return bitskins_items

    def generate_item(self, item_name):
        item_sales = self.get_sales_info_json(item_name)

        # no item sales on bitskins
        #todo return None
        if len(item_sales) == 0:
            return Item(item_name, 0)

        name = item_sales[0]["market_hash_name"]
        price = self.calculate_price(item_sales)
        return Item(name, round(price, 2))

    def calculate_price(self, item_sales):
        prices = []
        for sale in item_sales:
            days_ago = (datetime.now() - datetime.fromtimestamp(sale["sold_at"])).days
            if days_ago <= self.pricing_time_period:
                prices.append(float(sale["price"]))

        if len(prices) == 0 or len(prices) < self.pricing_min_amount_sold:
            return 0

        if self.exclude_extremes and len(prices) > 6:
            prices = self.exclude_extreme_prices(prices)

        if self.price_calculation == "average":
            return statistics.mean(prices)

        if self.price_calculation == "lowest":
            return min(prices)

    def exclude_extreme_prices(self, prices):
        new_prices = []
        for price in prices:
            amount_from_mean = abs(price - statistics.mean(prices))
            stdev = statistics.stdev(prices)
            if amount_from_mean <= stdev or amount_from_mean < price / 20:
                new_prices.append(price)
        return new_prices

    def get_sales_info_json(self, item_name):
        api_url = self.api_endpoint.format("get_sales_info", self.api_key, self.token_generator.now(), item_name)
        response = requests.get(api_url)
        return response.json()["data"]["sales"]
