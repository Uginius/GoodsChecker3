import json
import time
from random import randint
from threading import Thread

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from config import selenium_arguments, browser_path, today, req_headers
from utilites import check_dir


class PagesGetter(Thread):
    def __init__(self, platform, goods):
        super().__init__()
        self.platform = platform
        self.goods = goods
        self.use_selenium = platform in ['dns', 'baucenter']
        self.browser = None
        self.folder = f'htmls/{today}'
        self.loaded_html = None
        self.platform_results = {}
        self.soup = None

    def run(self):
        if self.platform != 'akson':  # only this platform
            return
        check_dir(self.folder)
        if self.use_selenium:
            self.initiate_browser()
        self.collect_data()
        self.save_json()

    def initiate_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument(selenium_arguments[0])
        options.add_argument(selenium_arguments[1])
        self.browser = webdriver.Chrome(service=Service(executable_path=browser_path), options=options)

    def collect_data(self):
        ll = len(self.goods)
        for order, row_id in enumerate(self.goods, 1):
            url = self.goods[row_id]['url']
            wait_time = randint(4, 9)
            print(f'{self.platform:>10} ({order} / {ll:03}), waiting: {wait_time} | connecting to url: {url}')
            self.get_page(url, wait_time)
            self.save_page(row_id)
            self.parse_page(row_id)

    def get_page(self, url, wait_time):
        try:
            if self.use_selenium:
                self.browser.get(url=url)
                time.sleep(wait_time)
                self.loaded_html = self.browser.page_source
            else:
                req = requests.get(url, headers=req_headers)
                time.sleep(wait_time)
                self.loaded_html = req.text
        except Exception as ex:
            print('getting data ERROR', '*' * 50, ex)
            self.loaded_html = None

    def parse_page(self, merch_id):
        self.soup = BeautifulSoup(self.loaded_html, 'lxml')
        try:
            match self.platform:
                case 'akson':
                    self.platform_results[merch_id] = self.parse_akson()
                case _:
                    pass
        except Exception as ex:
            print(f'Error on getting data from {merch_id}', '*' * 50, ex)

    def save_page(self, merch_id):
        filename = f'{self.folder}/{merch_id}_{self.platform}.html'
        with open(filename, 'w', encoding='utf8') as write_file:
            write_file.write(self.loaded_html)

    def save_json(self):
        with open(f'{self.folder}/{self.platform}.json', 'w', encoding='utf8') as fp:
            json.dump(self.goods, fp, ensure_ascii=False)

    def parse_akson(self):
        search_rating_value = self.soup.findAll('span', {"itemprop": "ratingValue"})
        if search_rating_value:
            rating_value = float(search_rating_value[0].text)
        else:
            return [None, None]
        review_count = int(self.soup.findAll('span', {"itemprop": 'reviewCount'})[0].text)
        return [rating_value, review_count]
