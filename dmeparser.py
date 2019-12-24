import requests
from bs4 import BeautifulSoup
import json
import re


def pars(stran: BeautifulSoup):
    mag = {}

    data = (stran.find('div', class_='shadows_left')
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
    for item in dan:
        if key and item.name == 'p' and 'располож' in item.text:
            pattern = re.compile('расположен[\w]?\s', re.IGNORECASE)
            mag[key]['location'] = re.split(pattern, item.text)[1]


        elif key and item.name == 'a' and item.text:
         mag_url = domain + (item.attrs["href"] if item.attrs['href'][0] == '/' else f'/{item.attrs["href"]}')
         mag[key]['shops'].append({'name': item.text, 'url': mag_url})

        elif item.name == 'h2':

         mag.update({item.text: {'name': item.text, 'location': 'неизвестно', 'mag': []}})
    key = item.text


    return mag

if __name__ == '__main__':
    url = 'https://www.dme.ru/shopping/shop/'

    domain = "".join(re.findall('(https?://)?(www\.)?([-\w.]+)', url)[0])

    stran = pol_stran(url)
    data = pars(stran)
    chten(data)

    stran = requests.get(url).text
    d = BeautifulSoup(page, 'lxml')
    data = pars(d)

    with open('parse_dme.json', 'w', encoding='utf-8') as f:
     json.dump(data, f, ensure_ascii=False)
