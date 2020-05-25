from datetime import datetime

from natasha import MorphVocab, AddrExtractor

from parsers import M24_accidents, Mosday_accidents, VM_accidents
from utils import get_news


def main():
    news_sites = {'m24.ru': M24_accidents,
                  'mosday.ru': Mosday_accidents,
                  'vm.ru': VM_accidents}

    # Инициализируем Наташу
    morph_vocab = MorphVocab()
    extractor = AddrExtractor(morph_vocab)

    # Ищем новости, проверяем на наличие адресов, загружаем
    # во временное хранилище
    news_list = []
    for key in news_sites.keys():
        try:
            ScrapeClass = news_sites.get(key)
            source = ScrapeClass()
            rec = get_news(source, extractor)
            news_list += rec
        except (TypeError):
            print("Источник {} недоступен.".format(key))

    for item in news_list:
        published = item['time'] + ' ' + item['date']
        published = datetime.strptime(published, '%H:%M %d.%m.%Y')

        print('-------------------------------------------------')
        print('title: ', item['title'])
        print('link: ,', item['link'])
        print('published: ', published)
        print('text: ', item['text'])
        print('address: ', item['location']['address'])
        print('street: ', item['location']['street'])
        print('lat :', item['location']['coordinates'][0])
        print('lon: ', item['location']['coordinates'][1])
    print('-------------------------------------------------')
    print(len(news_list))

    '''
    for item in news_list:
        if find_address_in_news(item, extractor):
            record = {
                'title': item['title'],
                'link': item['link'],
                'date_and_time': datetime.strptime(item['time'] + ' ' + item['date'], '%H:%M %d.%m.%Y'),
                'text': item['text'],
                'address': item['location']['address'],
                'street': item['location']['street'],
                'lat': item['location']['coordinates'][0],
                'lon': item['location']['coordinates'][1]
            }
            print(record)
            #db.session.add(record)
            #db.session.commit()
    '''

if __name__ == "__main__":
    main()
