import requests
import pyotp
from game import Item


class BitskinsAPI:

    def __init__(self, config):
        self.api_endpoint = config["bitskins"]["api_endpoint"]
        self.api_key = config["bitskins"]["api_key"]
        self.token_generator = pyotp.TOTP(config["bitskins"]["two_factor_secret"])
        self.min_amount_for_sale = config["bitskins"]["min_amount_for_sale"]

    def get_items(self):
        data = self.make_api_request("get_price_data_for_items_on_sale")
        items = []
        for item in data["data"]["items"]:
            name = item["market_hash_name"]
            price = item["lowest_price"]
            if item["total_items"] > self.min_amount_for_sale:
                items.append(Item(name, float(price)))
        return items

    def make_api_request(self, request_name):
        api_url = self.api_endpoint.format(request_name, self.api_key, self.token_generator.now())
        response = requests.get(api_url)
        return response.json()
