from bs4 import BeautifulSoup
from time import sleep
from game import Item
from selenium import webdriver

class CsdealsAPI:
    def __init__(self, config):
        self.min_price = config["csdeals_reload"]["min_price"]
        self.max_price = config["csdeals_reload"]["max_price"]
        self.url = config["csdeals_reload"]["url"]
        self.show_browser_window = config["csdeals_reload"]["show_browser_window"]

    def get_items(self):
        item_soup = self.get_item_soup()
        items = self.generate_items(item_soup)
        return items

    def generate_items(self, soup):
        items = []
        list_items = soup.findAll("div", {"class": "item"})

        for list_item in list_items:
            # todo optimize selecting item name and price
            item_name = str(list_item.find("img", {"class": "itemimg"}).get("alt"))

            price_and_discount_string = list_item.find("div", {"class": "price"}).text
            price_and_discount = price_and_discount_string.split("-")
            item_price=float(price_and_discount[0].replace("$","").replace(",","").replace("?%",""))
            items.append(Item(item_name, item_price))
        return items

    def get_item_soup(self):
        options = webdriver.ChromeOptions()
        if not self.show_browser_window:
            options.add_argument("--headless")
        driver = webdriver.Chrome("C:/Windows/chromedriver.exe", chrome_options=options)
        print("getting cs.deals items..")

        url = self.url.format(self.min_price,self.max_price)
        driver.get(url)

        new_height = driver.execute_script("return document.body.scrollHeight;")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
            height = driver.execute_script("return document.body.scrollHeight;")
            if height == new_height:
                break
            new_height = height

        return BeautifulSoup(driver.page_source,"html.parser")


