import requests
import re


def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except (requests.RequestException, ValueError):
        return None


def get_coordinates(address):
    '''
    Функция принимает строку с адресом и возвращает найденные коодинаты в виде
    кортежа (ширина, долгота).
    '''
    url = 'http://search.maps.sputnik.ru/search/addr?q=' + address
    r = requests.get(url).json()
    try:
        lats = []
        lons = []
        # вытаскиваем координаты из json (их обычно ищется несколько)
        # и считаем среднее
        for i in range(len(r['result']['address'])):
            for j in range(len(r['result']['address'][i]['features'])):
                for k in range(len(r['result']['address'][0]['features'][0]['geometry']['geometries'])):
                    lons.append(r['result']['address'][i]['features'][j]['geometry']['geometries'][0]['coordinates'][0])
                    lats.append(r['result']['address'][i]['features'][j]['geometry']['geometries'][0]['coordinates'][1])
        return sum(lats)/len(lats), sum(lons)/len(lons)
    except KeyError:
        return None


def extract_address(text, extractor):
    '''
    Функция принимает список OrderedDict-ов facts от Наташи, формирует из них
    адреса в виде строк
    "*название улицы/площади/др.* *улица/площадь/др.*, *номер дома*"
    проверяет, прогоняет через re.match, удаляет дубликаты и возвращает
    список строк в виде
    "Москва, *название улицы/площади/др.* *улица/площадь/др.*, *номер дома*
    '''
    address_types = ['улица', 'площадь', 'проезд', 'бульвар',
                     'переулок', 'проспект', 'шоссе']
    address_list = []  # список найденных в тексте адресов

    matches = extractor(text)
    facts = [item.fact.as_json for item in matches]
    try:
        for i in range(len(facts)):
            address = ''
            if facts[i]['type'] in address_types:
                address += facts[i]['value'] + ' ' + facts[i]['type']
                for j in range(-1, 2):
                    try:
                        if facts[i+j]['type'] == 'дом':
                            address += ', ' + facts[i+j]['value']
                    except IndexError:
                        continue
                # Дополнительная проверка (название улицы - с большой буквы)
                if re.match(r'([А-Я]|\d*\-[а-я] [А-Я])', address):
                    address_list.append('Москва, ' + address)
                #address_list.append('Москва, ' + address)
                address_list = list(set(address_list))
        return address_list
    except KeyError:
        return None 


def find_address_in_news(item, extractor):
    for_record = False
    address_list = extract_address(item['text'], extractor)
    if address_list:
        street = address_list[0].split(',')[1].strip()
        item['location'] = {'address': address_list,
                            'street': street}
        item['location']['coordinates'] = get_coordinates(address_list[0])
        if item['location']['coordinates']:
            for_record = True
    return for_record


def get_news(source, extractor):
    news_with_location = []
    results = source.get_feed()
    for item in results:
        item['text'] = source.get_post(item['link']).replace('\n', '')
        # если есть текст новости - ищем в ней адреса
        if item['text']:
            if find_address_in_news(item, extractor):
                news_with_location.append(item)
    return news_with_location

