from os import path
import json
import pickle
from bitskins_api import BitskinsAPI
from buff_api import BuffAPI
from csdeals_api import CsdealsAPI


def find_item(items, item_to_find):
    return next((item for item in items if item == item_to_find), None)


def get_comparisons(items_to_buy, items_to_sell, buy_platform, sell_platform):
    item_comparisons = []
    for item_to_buy in items_to_buy:
        item_to_sell = find_item(items_to_sell, item_to_buy)
        if item_to_sell:
            price_difference = item_to_sell.price - item_to_buy.price
            discount = 0
            if item_to_sell.price != 0:
                discount = round(100 * price_difference / item_to_sell.price, 2)
            comparison = {
                buy_platform: item_to_buy,
                sell_platform: item_to_sell,
                "discount": discount
            }

            item_comparisons.append(comparison)
    return item_comparisons


def sort_item_comparisons(item_comparisons):
    return sorted(item_comparisons, key=lambda i: i['discount'], reverse=True)


def get_config():
    try:
        with open('config.json') as json_file:
            return json.load(json_file)
    except FileNotFoundError as fnf_error:
        print(fnf_error)


class ItemComparator:
    def __init__(self):
        config = get_config()
        self.bitskins_api = BitskinsAPI(config)
        self.buff_api = BuffAPI(config)
        self.csdeals_api = CsdealsAPI(config)
        self.buy_mode = config["main"]["buy_mode"]
        self.items_local_storage_path = config["main"]["items_local_storage_path"]
        self.reload_all_items = config["main"]["reload_all_items"]
        self.buy_min_price = config["comparison_settings"]["buy_min_price"]
        self.buy_max_price = config["comparison_settings"]["buy_max_price"]
        self.buff_items = []
        self.bitskins_items = []
        self.csdeals_items = []

    def start(self):
        self.load_items()
        items_to_buy = []
        items_to_sell = []
        buy_platform = self.buy_mode
        sell_platform = "bitsksins" if buy_platform == "buff" else "buff"
        if self.buy_mode == "buff":
            items_to_buy = self.buff_items
            items_to_sell = self.bitskins_items
        elif self.buy_mode == "csdeals":
            items_to_buy = self.csdeals_items
            items_to_sell = self.buff_items
        elif self.buy_mode == "bitsksins":
            items_to_buy = self.bitskins_items
            items_to_sell = self.buff_items
        else:
            print("wrong buy mode in config defined. Correct buy modes are 'buff' or 'csdeals'")

        item_comparisons = get_comparisons(items_to_buy, items_to_sell, buy_platform, sell_platform)
        item_comparisons_filtered = self.filter_comparisons(item_comparisons, buy_platform)
        item_comparisons_sorted = sort_item_comparisons(item_comparisons_filtered)
        self.show_item_comparisons(item_comparisons_sorted, buy_platform, sell_platform)

    def show_item_comparisons(self, item_comparisons, buy_platform, sell_platform):

        for comparison in item_comparisons:
            print("discount on " + buy_platform + ": " + str(comparison["discount"])
                  + "% " + buy_platform + " price: " + str(comparison[buy_platform].price)
                  + " " + sell_platform + " price: " + str(comparison[sell_platform].price)
                  + " name: " + comparison[buy_platform].name)

    def filter_comparisons(self, comparisons, buy_platform):
        comparisons_filtered = []
        for comparison in comparisons:
            if self.buy_min_price <= comparison[buy_platform].price <= self.buy_max_price:
                comparisons_filtered.append(comparison)

        return comparisons_filtered

    def load_items(self):
        if self.reload_all_items or not path.exists(
                self.items_local_storage_path + "/buff_items.pkl") or not path.exists(
            self.items_local_storage_path + "/bitskins_items.pkl") or not path.exists(
            self.items_local_storage_path + "/csdeals_items.pkl"):
            buff_items = self.buff_api.get_items()
            csdeals_items = self.csdeals_api.get_items()
            bitskins_items = self.bitskins_api.get_items(buff_items)
            pickle.dump(buff_items, open(self.items_local_storage_path + "/buff_items.pkl", "wb"))
            pickle.dump(bitskins_items, open(self.items_local_storage_path + "/bitskins_items.pkl", "wb"))
            pickle.dump(csdeals_items, open(self.items_local_storage_path + "/csdeals_items.pkl", "wb"))

        self.buff_items = pickle.load(open(self.items_local_storage_path + '/buff_items.pkl', "rb"))
        self.bitskins_items = pickle.load(open(self.items_local_storage_path + '/bitskins_items.pkl', "rb"))
        self.csdeals_items = pickle.load(open(self.items_local_storage_path + '/csdeals_items.pkl', "rb"))
