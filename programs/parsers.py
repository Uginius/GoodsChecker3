from bs4 import BeautifulSoup


def parse_akson(soup):
    search_rating_value = soup.findAll('span', {"itemprop": "ratingValue"})
    if search_rating_value:
        rating_value = float(search_rating_value[0].text)
    else:
        return [None, None]
    review_count = int(soup.findAll('span', {"itemprop": 'reviewCount'})[0].text)
    return [rating_value, review_count]


def parse_baucenter(soup):
    product = soup.find('section', class_='product')
    rev_count = product.find('span', class_='catalog_item_rating_rev-count')
    review_count = int(rev_count.text.strip())
    percent = int(product.find('div', class_='raiting-votes')['style'].split(': ')[1][:-2])
    rating_value = round((percent * 5) / 100, 2)
    return [rating_value, review_count]


def parse_dns(soup):
    votes = soup.find('a', class_='product-card-top__rating ui-link ui-link_black')
    rating_value = float(votes['data-rating'])
    vote_qt = votes.text.strip()
    if vote_qt == 'нет отзывов':
        vote_qt = 0
    review_count = int(vote_qt)
    return [rating_value, review_count]


def parse_maxidom(soup):
    rating_value = float(soup.find('div', class_='score__number').text)
    grades = soup.find('div', class_='score-rating').find_all('div', class_='scale__number')
    review_count = sum(int(mark.text) for mark in grades)
    return [rating_value, review_count]


def parse_sdvor(soup):
    rating = soup.find('div', class_='rating').find_all('span')
    rating_value = float(rating[0].text[1:-1])
    review_count = int(rating[1].text.split()[0])
    return [rating_value, review_count]


def parse_votonia(soup):
    rating_value, review_count = None, None
    return [rating_value, review_count]


parsers = {'akson': parse_akson, 'baucenter': parse_baucenter, 'dns': parse_dns, 'maxidom': parse_maxidom,
           'sdvor': parse_sdvor, 'votonia': parse_votonia, }

if __name__ == '__main__':
    filename = r'C:\work\python_projects\GoodsChecker3\htmls\2022-08-04\362_maxidom.html'
    with open(filename, 'r', encoding='utf8') as read_file:
        src = read_file.read()
    result = parsers['maxidom'](BeautifulSoup(src, 'lxml'))
    print(result)
