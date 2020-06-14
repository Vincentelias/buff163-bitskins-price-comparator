import requests
import pyotp
from game import Item

class BitskinsAPI:

    def __init__(self, config):
        self.app_id = self.get_app_id(config["main"]["game"])
        self.api_endpoint = config["main"]["bitskins_api_endpoint"]
        self.api_key = config["main"]["bitskins_api_key"]
        self.token_generator = pyotp.TOTP(config["main"]["two_factor_secret"])
        self.min_amount_for_sale = config["main"]["min_amount_for_sale"]

    def get_items(self):
        # csgo
        if self.app_id == 730:
            data = self.make_api_request("get_price_data_for_items_on_sale")
            items = []
            for item in data["data"]["items"]:
                name = item["market_hash_name"]
                price = item["lowest_price"]
                if item["total_items"] > self.min_amount_for_sale:
                    items.append(Item(name, float(price)))
            return items

    def get_app_id(self, game):
        try:
            if game == "csgo":
                return 730
            if game == "dota2":
                return 570
            raise Exception("Invalid game name entered. Allowed games are 'csgo' and 'dota2'")
        except Exception as error:
            print(error)

    def make_api_request(self, request_name):
        api_url = self.api_endpoint.format(request_name, self.api_key, self.token_generator.now(), self.app_id)
        response = requests.get(api_url)
        return response.json()
