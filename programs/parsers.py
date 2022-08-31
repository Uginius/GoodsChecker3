import json
from bs4 import BeautifulSoup


def parse_akson(loaded_html):
    soup = BeautifulSoup(loaded_html, 'lxml')
    search_rating_value = soup.findAll('span', {"itemprop": "ratingValue"})
    if search_rating_value:
        rating_value = float(search_rating_value[0].text)
    else:
        return [None, None]
    review_count = int(soup.findAll('span', {"itemprop": 'reviewCount'})[0].text)
    return [rating_value, review_count]


def parse_baucenter(loaded_html):
    soup = BeautifulSoup(loaded_html, 'lxml')
    product = soup.find('section', class_='product')
    rev_count = product.find('span', class_='catalog_item_rating_rev-count')
    review_count = int(rev_count.text.strip())
    percent = int(product.find('div', class_='raiting-votes')['style'].split(': ')[1][:-2])
    rating_value = round((percent * 5) / 100, 2)
    return [rating_value, review_count]


def parse_dns(loaded_html):
    soup = BeautifulSoup(loaded_html, 'lxml')
    votes = soup.find('a', class_='product-card-top__rating ui-link ui-link_black')
    rating_value = float(votes['data-rating'])
    vote_qt = votes.text.strip()
    if vote_qt == 'нет отзывов':
        vote_qt = 0
    review_count = int(vote_qt)
    return [rating_value, review_count]


def parse_maxidom(loaded_html):
    soup = BeautifulSoup(loaded_html, 'lxml')
    rating_value = float(soup.find('div', class_='score__number').text)
    grades = soup.find('div', class_='score-rating').find_all('div', class_='scale__number')
    review_count = sum(int(mark.text) for mark in grades)
    return [rating_value, review_count]


def parse_sdvor(loaded_html):
    data = json.loads(loaded_html)
    rating = data['Stats']
    review_count = rating['Rate5TotalCount']
    rating_value = float(rating['RatesTotalSum'] / review_count)
    return [rating_value, review_count]


def parse_votonia(loaded_html):
    soup = BeautifulSoup(loaded_html, 'lxml')
    tab_review = soup.find('div', id="tab-review").find('div', class_='row').div
    line = tab_review.find('div', class_='review_info_line')
    rating_value = float(line.b.text.strip().replace('"', ''))
    review_count = int(line.text.strip().split()[-2])
    return [rating_value, review_count]


parsers = {'akson': parse_akson, 'baucenter': parse_baucenter, 'dns': parse_dns, 'maxidom': parse_maxidom,
           'sdvor': parse_sdvor, 'votonia': parse_votonia, }

if __name__ == '__main__':
    filename = r'C:\work\python_projects\GoodsChecker3\htmls\2022-08-04\362_maxidom.html'
    with open(filename, 'r', encoding='utf8') as read_file:
        src = read_file.read()
    result = parsers['maxidom'](BeautifulSoup(src, 'lxml'))
    print(result)
