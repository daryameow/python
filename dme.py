from bs4 import BeautifulSoup
import requests
import json
import re


url = 'https://www.dme.ru/shopping/shop/'
domain = "".join(re.findall('(https?://)?(www\.)?([-\w.]+)', url)[0])


page_dme = requests.get(url).text
parse_dme =BeautifulSoup(page_dme, 'lxml')






def parse(page_dme: BeautifulSoup):
    shops = {}

   
    data = (page_dme.find('div', class_='shadows_left')
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

        elif key and item.name == 'p' and 'располож' in item.text:
            
            pattern = re.compile('расположен[\w]?\s', re.IGNORECASE)
            shops[key]['location'] = re.split(pattern, item.text)[1]

        elif key and item.name == 'a' and item.text:
            shop_url = domain + (item.attrs["href"] if item.attrs['href'][0] == '/' else f'/{item.attrs["href"]}')
            shops[key]['shops'].append({'name': item.text, 'url': shop_url})

    return shops

data = parse(parse_dme)

with open('parse_dme.json', 'w', encoding='utf-8') as f:
     json.dump(data, f, ensure_ascii=False)
