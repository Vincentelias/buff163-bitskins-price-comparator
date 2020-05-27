from bs4 import BeautifulSoup
from time import sleep
from game import Item
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BuffAPI:

    def __init__(self, config):
        self.config = config
        self.game = config["main"]["game"]
        self.min_price = config["csgo"]["min_price"]
        self.max_price = config["csgo"]["max_price"]
        self.category_group = config["csgo"]["category_group"]
        self.quality = self.generate_quality(config["csgo"]["show_stattrak"])
        self.buff_api_endpoint = config["main"]["buff_api_endpoint"]
        self.buff_session_id = config["main"]["buff_session_id"]
        self.request_interval = config["main"]["request_interval"]
        self.show_browser_window = config["main"]["show_browser_window"]

    def get_items(self):
        item_soups = self.get_item_soups()
        items = self.generate_items(item_soups)
        return items

    def generate_quality(self, show_stattrak):

        #todo optimize stattrak readings
        if show_stattrak:
            if self.category_group == "knife":
                return "unusual_strange"
            else:
                return ""

        else:
            if self.category_group == "knife":
                return "unusual"
            else:
                return "normal"

    def generate_items(self, item_soups):
        items = []
        for soup in item_soups:
            list_items = soup.find_all("li")
            for list_item in list_items:
                #todo optimize selecting item name and price
                item_name = str(list_item.find_all("a")[0].get("title"))
                item_price_string = str(list_item.find("strong", {"class": "f_Strong"}))
                price_array = re.findall(r'\d+', item_price_string)
                if len(price_array) == 1:
                    price_array.append("0")
                item_price = float(price_array[0] + "." + price_array[1])
                items.append(Item(item_name, item_price))
        return items

    def get_item_soups(self):
        options = webdriver.ChromeOptions()
        if not self.show_browser_window:
            options.add_argument("--headless")

        driver = webdriver.Chrome("./chromedriver", chrome_options=options)
        print("setting session id..")
        self.set_cookie_session(driver)
        current_page = 1
        has_next_page = True
        item_soups = []

        print("retrieving pages..")
        while has_next_page:
            page_source = self.get_page_html(current_page, driver)
            items_soup = BeautifulSoup(page_source, "html.parser").find_all("ul", {"class": "card_csgo"})[0]
            has_next_page = str(BeautifulSoup(page_source, "html.parser").find("span", {"class": "current"})) != "None"
            current_page += 1
            item_soups.append(items_soup)
            sleep(self.request_interval)
        return item_soups

    def get_page_html(self, page, driver):
        api_url = self.buff_api_endpoint.format(self.game, page, self.category_group, self.min_price,
                                                self.max_price, self.quality)
        driver.get(api_url)
        driver.refresh()
        try:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CLASS_NAME, "card_csgo"))
            )
        except Exception:
            driver.quit()
            print("Unable to get skins from page "+str(page))

        print("retrieved buff.163 page " + str(page))
        return driver.page_source

    def set_cookie_session(self, driver):
        driver.get("http://buff.163.com")
        driver.maximize_window()
        driver.add_cookie({"name": "session", "value": self.buff_session_id})
        print("succesfully set session id")
