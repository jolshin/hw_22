import requests
import bs4
from datetime import date

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

date_ = []
headline = []
link_ = []

cookies = {
    'habr_web_home_feed': '/all/',
    'hl': 'ru',
    'fl': 'ru',
    'tildauid': '1664279500003.879794',
    'visited_articles': '55254:406327:517500:488054:190336',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'habr_web_home_feed=/all/; hl=ru; fl=ru; tildauid=1664279500003.879794; visited_articles=55254:406327:517500:488054:190336',
    'Referer': 'https://github.com/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

url_all = 'https://habr.com'

response = requests.get(url_all, cookies=cookies, headers=headers).text

soup = bs4.BeautifulSoup(response, features='html.parser')

articles = soup.find_all('article')

for article in articles:
    url_ = str(url_all + article.find(class_ = 'tm-article-snippet__title-link').attrs['href'])
    response_ = requests.get(url_, cookies=cookies, headers=headers).text

    soup_ = bs4.BeautifulSoup(response_, features='html.parser')

    article_body = soup_.find(class_ = 'tm-article-body').text

    for word in KEYWORDS:
        match = [x for x in headline if x == soup_.find('h1').text]

        if not match:
            if word in article_body:
                if 'сегодня' in soup_.find('time').text:
                    today_date = str(date.today().strftime('%d %B')) + soup_.find('time').text[7:]
                    date_.append(today_date)
                else:
                    date_.append(soup_.find('time').text)
                headline.append(soup_.find('h1').text)
                link_.append(url_)

for i in range(len(headline)):
    print(date_[i-1], end=' -- ')
    print(headline[i-1], end=' -- ')
    print(link_[i-1])