from bitskins_api import BitskinsAPI
from buff_api import BuffAPI

import json

try:
    with open('config.json') as json_file:
        config = json.load(json_file)
except FileNotFoundError as fnf_error:
    print(fnf_error)

print("starting..")

bitskins_api = BitskinsAPI(config)
buff_api = BuffAPI(config)

bitskins_items = bitskins_api.get_items()
buff_items = buff_api.get_items()
print(len(buff_items))

item_comparisons = []
#todo swap for loops and split into functions
for bitskins_item in bitskins_items:
    for buff_item in buff_items:
        if bitskins_item == buff_item:
            price_difference=bitskins_item.price-buff_item.price
            discount=0
            if bitskins_item.price!=0:
                discount = round(100*price_difference/bitskins_item.price,2)
            comparison = {
                "buff": buff_item,
                "bitskins": bitskins_item,
                "discount": discount
            }

            item_comparisons.append(comparison)

comparisons_sorted=sorted(item_comparisons, key = lambda i: i['discount'],reverse=True)

for comparison in comparisons_sorted:
    print("discount on buff: "+str(comparison["discount"])
          +"% buff price: "+str(comparison["buff"].price)
          +" bitskins price: "+str(comparison["bitskins"].price)
          +" name: "+comparison["buff"].name)
