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
        self.min_price = config["buff_reload"]["min_price"]
        self.max_price = config["buff_reload"]["max_price"]
        self.category_group = config["buff_reload"]["category_group"]
        self.quality = config["buff_reload"]["quality"]
        self.url = config["buff_reload"]["url"]
        self.buff_session_id = config["buff_reload"]["session_id"]
        self.request_interval = config["buff_reload"]["request_interval"]
        self.show_browser_window = config["buff_reload"]["show_browser_window"]

    def get_items(self):
        item_soups = self.get_item_soups()
        items = self.generate_items(item_soups)
        return items


    def generate_items(self, item_soups):
        items = []
        for soup in item_soups:
            list_items = soup.find_all("li")
            for list_item in list_items:
                # todo optimize selecting item name and price
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

        driver = webdriver.Chrome("C:/Windows/chromedriver.exe", chrome_options=options)
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
        url = self.url.format(page, self.category_group, self.min_price,
                                                self.max_price, self.quality)
        driver.get(url)
        driver.refresh()

        try:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CLASS_NAME, "card_csgo"))
            )
        except Exception:
            driver.quit()
            print("Unable to get skins from page " + str(page))

        print("retrieved buff page " + str(page))
        return driver.page_source

    def set_cookie_session(self, driver):
        driver.get("http://buff.163.com")
        driver.maximize_window()
        driver.add_cookie({"name": "session", "value": self.buff_session_id})
        print("succesfully set session id")
