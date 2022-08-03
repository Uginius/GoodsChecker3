from programs.pages_getter import PagesGetter
from tmp.parse_akson import parse_akson
from utilites import read_table, time_track


@time_track
def get_pages(path):
    getters = [PagesGetter(platform, goods) for platform, goods in read_table(path).items()]
    for getter in getters:
        getter.start()
    for getter in getters:
        getter.join()


if __name__ == '__main__':
    table_name = 'src/goods_tp.xlsx'
    get_pages(table_name)
