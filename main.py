from programs.create_result_table import update_result_table
from programs.pages_getter import PagesGetter
from utilites import read_table, time_track

table_name = 'src/goods_tp.xlsx'
correct_table_name = 'src/rosel_products.xlsx'


@time_track
def get_pages():
    getters = [PagesGetter(platform, goods) for platform, goods in read_table(table_name).items()]
    for getter in getters:
        getter.start()
    for getter in getters:
        getter.join()


@time_track
def data_to_xls():
    update_result_table(table_name)


if __name__ == '__main__':
    get_pages()
    data_to_xls()
