from bitskins_api import BitskinsAPI
from buff_api import BuffAPI
from game import Item

import json


def find_item(items, other):
    return next((item for item in items if item==other), None)


try:
    with open('config.json') as json_file:
        config = json.load(json_file)
except FileNotFoundError as fnf_error:
    print(fnf_error)


print("starting..")

bitskins_api = BitskinsAPI(config)
buff_api = BuffAPI(config)

buff_items = buff_api.get_items()
bitskins_items = bitskins_api.get_items(buff_items)


item_comparisons = []

for buff_item in buff_items:
    bitskins_item = find_item(bitskins_items, buff_item)

    price_difference = bitskins_item.price - buff_item.price
    discount = 0
    if bitskins_item.price != 0:
        discount = round(100 * price_difference / bitskins_item.price, 2)
    comparison = {
        "buff": buff_item,
        "bitskins": bitskins_item,
        "discount": discount
    }

    item_comparisons.append(comparison)

comparisons_sorted = sorted(item_comparisons, key=lambda i: i['discount'], reverse=True)

for comparison in comparisons_sorted:
    if comparison["bitskins"].price!=0:
        print("discount on buff: " + str(comparison["discount"])
              + "% buff price: " + str(comparison["buff"].price)
              + " bitskins price: " + str(comparison["bitskins"].price)
              + " name: " + comparison["buff"].name)
