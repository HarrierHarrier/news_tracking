from datetime import datetime

from bs4 import BeautifulSoup

from utils import get_html


class M24_accidents(object):
    def __init__(self):
        self.url = 'https://www.m24.ru'

    def get_feed(self):
        html = get_html(self.url + '/tag/происшествия')
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            html_class = 'b-materials-list b-list_infinity'
            news_found = soup.find('div', class_=html_class)
            news_found = news_found.find('ul').find_all('li')
            result_news = []
            for item in news_found:
                news = item.find('p', class_='b-materials-list__title')
                news = news.find('a')

                title = news.text.strip('\n\t')
                link = self.url + news['href']
                time = item.find('span').text
                date = datetime.now().strftime('%d.%m.%Y')

                result_news.append({
                    'title': title,
                    'link': link,
                    'time': time,
                    'date': date
                })
            return result_news
        else:
            return None

    def get_post(self, url):
        html = get_html(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            # есть страницы с разной разметкой, except - страницы
            #  с видео и парой абзацев
            try:
                html_class = 'js-mediator-article'
                text_blocks = soup.find('div', class_=html_class)
                text_blocks = text_blocks.find_all('p', class_='')
            except AttributeError:
                html_class = 'b-material-body'
                text_blocks = soup.find('div', class_=html_class)
                text_blocks = text_blocks.find_all('p', class_='')

            news_text = ''
            for block in text_blocks:
                block = block.text.replace('\xa0\n', '')
                news_text += block.strip('\n\t ') + '\n'
            return news_text
        else:
            return None


class Mosday_accidents(object):
    def __init__(self):
        self.url = 'http://mosday.ru/news'

    def get_feed(self):
        html = get_html(self.url + '/tags.php?accident')
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            news_found = soup.find('body').find('table', width="100%",
                                                height="500", cellpadding="0",
                                                cellspacing="0", border="0")
            news_found = news_found.find('table', width="100%",
                                         cellpadding="0", cellspacing="10",
                                         border="0")
            news_found = news_found.find('center')
            style = "font-family:Arial;font-size:15px"
            news_found = news_found.find('table', width="95%",
                                         cellpadding="0", cellspacing="10",
                                         border="0",
                                         style=style)
            news_found = news_found.find_all('font', face="Arial", size="2",
                                             color="#666666",
                                             style="font-size:13px")
            result_news = []
            for item in news_found:
                title = item.find('a').text
                link = self.url + '/' + item.find('a')['href']
                date = item.find('b').text
                time = item.text[12:16]
                result_news.append({'title': title,
                                    'link': link,
                                    'time': time,
                                    'date': date})
            return result_news
        else:
            return None

    def get_post(self, url):
        html = get_html(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            text_blocks = soup.find('table', width="100%", cellpadding="0",
                                    cellspacing="10", border="0")
            text_blocks = text_blocks.find('article', itemprop="articleBody")
            text_blocks = text_blocks.find('div', itemprop="text")
            text_blocks = text_blocks.find_all('p')

            news_text = ''
            for block in text_blocks:
                block = block.text.replace('\xa0\n', '')
                news_text += block.strip('\n\t ') + '\n'
            return news_text
        else:
            return None


class VM_accidents(object):
    def __init__(self):
        self.url = 'https://vm.ru'

    def get_feed(self):
        html = get_html(self.url + '/accidents')
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            news_found = soup.find('div', class_='articles-list')
            html_class = 'articles-list__item'
            news_found = news_found.find_all('div', class_=html_class)
            result_news = []
            for item in news_found:
                title = item.find('a').text.replace('\xa0\n', '')
                title = title.strip('\n\t ')

                link = self.url + item.find('a')['href']

                published = item.find('ul')
                html_class = 'articles-list__info articles-list__info--time'
                time = published.find('li', class_=html_class).text
                time = time.strip('\n\t')

                html_class = 'articles-list__info articles-list__info--date'
                day = published.find('li', class_=html_class).text
                day = str(int(day.strip('\n\t')[0:2]))
                month_and_year = datetime.now().strftime('.%m.%Y')
                date = day + month_and_year

                result_news.append({
                    'title': title,
                    'link': link,
                    'time': time,
                    'date': date
                })
            return result_news
        else:
            return None

    def get_post(self, url):
        html = get_html(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            html_class = 'single-article__main-content'
            text_blocks = soup.find('div', class_=html_class).find_all('p')
            text_blocks = text_blocks[:-1]
            news_text = ''
            for block in text_blocks:
                block = block.text.replace('\xa0', '').strip('\n\t ')
                news_text += block + '\n'
            return news_text
        else:
            return None


if __name__ == "__main__":
    print(
        """Проверка работы парсеров. Доступны парсеры для сайтов:
      m24.ru - 1;
      mosday.ru - 2:
      vm.ru - 3.

Для проверки введите номер парсера (1, 2 или 3), чтобы выйти, нажмите Enter.
        """)
    inp = input()
    if inp in ['1', '2', '3']:
        if inp == '1':
            parser = M24_accidents()
        elif inp == '2':
            parser = Mosday_accidents()
        elif inp == '3':
            parser = VM_accidents()
        parser = VM_accidents()
        feed = parser.get_feed()

        for news in feed:
            print('----------------------')
            print(news)
            print()
            text = parser.get_post(news['link'])
            if text:
                if len(text) > 250:
                    print(text)
                else:
                    print("Полный текст новости в источнике.")
        print('----------------------')
        print(len(feed))
    else:
        print("Номер парсера не введен.\nВыход...")
