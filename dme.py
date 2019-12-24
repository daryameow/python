from bs4 import BeautifulSoup
import requests
import json
import re


url = 'https://www.dme.ru/shopping/shop/'
domain = "".join(re.findall('(https?://)?(www\.)?([-\w.]+)', url)[0])


page = requests.get(url).text
d=BeautifulSoup(page, 'lxml')






def parse(page: BeautifulSoup):
    shops = {}

    # Добираемся до списка магазинов
    data = (page.find('div', class_='shadows_left')
            .find('div', class_='shadows_right')
            .find('div', class_='layout')
            .find('div', class_='main')
            .find('div', class_='right_column')
            .find('div', class_='content')
            .find('div', class_='simple')
            .find('div', class_='simple')
            .find('div')
            .find('div'))

    # Ищем все заголовки, ссылки, абзацы (в них расположена информация о магазинах)
    data = data.findAll(['a', 'h2', 'p'])

    key = ''
    for item in data:
        if item.name == 'h2':
            # Создаем новый раздел, если находим заголовок (название раздела)
            shops.update({item.text: {'name': item.text, 'location': 'неизвестно', 'shops': []}})
            key = item.text

        elif key and item.name == 'p' and 'располож' in item.text:
            # Преобразовываем и записываем местоположение магазинов, если находим таковое
            pattern = re.compile('расположен[\w]?\s', re.IGNORECASE)
            shops[key]['location'] = re.split(pattern, item.text)[1]

        elif key and item.name == 'a' and item.text:
            shop_url = domain + (item.attrs["href"] if item.attrs['href'][0] == '/' else f'/{item.attrs["href"]}')
            shops[key]['shops'].append({'name': item.text, 'url': shop_url})

    return shops

data = parse(d)

with open('Timoha2.json', 'w', encoding='utf-8') as f:
     json.dump(data, f, ensure_ascii=False)