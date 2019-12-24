from bs4 import BeautifulSoup
import requests
import json
import re


def write(data: dict):
    
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
url = 'https://www.dme.ru/shopping/shop/'


domain = "".join(re.findall('(https?://)?(www\.)?([-\w.]+)', url)[0])



def get_page(url: str):
    
    page = requests.get(url).text
    return BeautifulSoup(page, 'lxml')


def parse(page: BeautifulSoup):
    shops = {}

    
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

    
    data = data.findAll(['a', 'h2', 'p'])

    key = ''
    for item in data:
        if item.name == 'h2':
            
            shops.update({item.text: {'name': item.text, 'location': 'неизвестно', 'shops': []}})
            key = item.text

        elif key and item.name == 'p' and 'расположен' in item.text:
            
            shops[key]['location'] = item.text

        elif key and item.name == 'a' and item.text:
            shop_url = domain + (item.attrs["href"] if item.attrs['href'][0] == '/' else f'/{item.attrs["href"]}')
            shops[key]['shops'].append({'name': item.text, 'url': shop_url})

    return shops



page = get_page(url)
data = parse(page)
write(data)