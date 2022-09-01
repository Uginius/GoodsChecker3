import json
import time
from random import randint
from threading import Thread
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from config import selenium_arguments, browser_path, today, req_headers
from programs.parsers import parsers
from utilites import check_dir


class PagesGetter(Thread):
    def __init__(self, platform, goods):
        super().__init__()
        self.platform = platform
        self.goods = goods
        self.use_selenium = platform in ['dns']
        self.browser = None
        self.folder = f'htmls/{today}'
        self.loaded_html = None
        self.platform_results = {}
        self.soup = None
        self.row_id = None

    def run(self):
        # if self.platform not in ['votonia']:  # only this
        #     return
        check_dir(self.folder)
        if self.use_selenium:
            self.initiate_browser()
        self.collect_data()
        if self.browser:
            self.browser.close()
        self.save_json()

    def initiate_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument(selenium_arguments[0])
        options.add_argument(selenium_arguments[1])
        self.browser = webdriver.Chrome(service=Service(executable_path=browser_path), options=options)

    def collect_data(self):
        ll = len(self.goods)
        shop = self.platform
        for order, self.row_id in enumerate(self.goods, 1):
            row_id = self.row_id
            url = self.goods[row_id]['url']
            wait_time = randint(4, 9)
            print(f'{shop :>10} ({order:03}/{ll:03}), row: {row_id}, wait: {wait_time} | connect to url: {url}')
            self.get_page(url, wait_time)
            self.save_page(row_id)
            self.parse_page(row_id)
        print('-' * 30, f'{shop} data collected', '-' * 30)

    def get_page(self, link, wait_time):
        url = self.set_url(link)
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

    def set_url(self, link):
        match self.platform:
            case 'maxidom':
                merch_id = self.goods[self.row_id]['shop id']
                url = f'https://www.maxidom.ru/ajax/mneniya_pro/getReviewsHtml.php?SKU_ID={merch_id}'
            case 'sdvor':
                merch_id = self.goods[self.row_id]['shop id']
                url = f'https://www.sdvor.com/api/mneniya-pro/v1.3/reviews/Product/{merch_id}/All'
            case _:
                url = link
        return url

    def parse_page(self, row_id):
        platform = self.platform
        try:
            self.platform_results[row_id] = parsers[platform](self.loaded_html)
        except Exception as ex:
            self.platform_results[row_id] = [None, None]
            print(f'Error on getting data from {row_id}_{platform}', '*' * 50, ex)

    def save_page(self, merch_id):
        filename = f'{self.folder}/{merch_id}_{self.platform}.html'
        with open(filename, 'w', encoding='utf8') as write_file:
            write_file.write(self.loaded_html)

    def save_json(self):
        with open(f'{self.folder}/{self.platform}.json', 'w', encoding='utf8') as fp:
            json.dump(self.platform_results, fp, ensure_ascii=False)
