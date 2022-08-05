import json
import os
from utilites import get_last_dir
from openpyxl import load_workbook


def read_data_from_json():
    folder = 'htmls/' + get_last_dir()
    json_files = [filename for filename in os.listdir(folder) if 'json' in filename]
    data = {}
    for filename in json_files:
        with open(f'{folder}/{filename}', 'r', encoding='utf8') as rf:
            data.update(json.load(rf))
    return data


def update_table(table, data):
    ws = table.active
    for order, row in enumerate(ws, 1):
        if order < 2:
            continue
        parser_id = f'{order:03}'
        rating_cell = row[4]
        votes_cell = row[5]
        value = data.get(parser_id)
        if not value:
            continue
        rating_cell.value, votes_cell.value = value


def update_result_table(xls_table):
    data = read_data_from_json()
    update_table(load_workbook(xls_table), data)
