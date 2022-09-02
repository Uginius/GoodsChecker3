import os
import re
import time
from datetime import datetime
from openpyxl import load_workbook
from config import dir_date_template, date_pattern, markets


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()
        result = func(*args, **kwargs)
        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        print(f'\nIt takes {elapsed:.3f} sec, or {elapsed / 60:.3f} min')
        return result

    return surrogate


def check_dir(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except Exception as ex:
        print(ex)



def get_last_dir(folder='htmls'):
    pages_dir_from_os = os.listdir(folder)
    loaded_dirs = []
    for el in pages_dir_from_os:
        checking_dir = re.findall(dir_date_template, el)
        try:
            if checking_dir:
                dir_in_list = datetime.strptime(el, date_pattern)
                loaded_dirs.append(dir_in_list)
        except ValueError as ex:
            print(ex)
    final_dir = sorted(loaded_dirs)[-1].strftime(date_pattern)
    return final_dir


def get_platform(shop_url):
    for shop in markets:
        if shop in shop_url:
            return shop
    return None


def read_table(table_name):
    workbook = load_workbook(table_name)
    stock = {}
    for order, row in enumerate(workbook.active, 1):
        if order < 2:
            continue
        parser_id = f'{order:03}'
        shop = row[0].value
        if not stock.get(shop):
            stock[shop] = {}
        stock[shop].update({parser_id: {'shop id': row[1].value, 'url': row[3].value}})
    workbook.close()
    return stock
