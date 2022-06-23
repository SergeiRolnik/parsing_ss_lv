import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import time
import json
import pandas as pd

#################################!!! ВАЖНО !!!###################################################
# Перед запуском кода, укажите специальность, например, Педагог, Кузнец, Сборщик
# Список специальностей находится в файле professions.json
PROFESSION = 'Садовник'
#################################################################################################

def make_clickable(url, name):
    return '=HYPERLINK("{}"; "{}")'.format(url, name)

file = open('professions.json', 'r', encoding='utf-8')
professions_urls = json.load(file)
file.close()
profession_url = professions_urls[PROFESSION.lower().capitalize()]
ua = UserAgent()
BASE_URL = 'https://www.ss.lv'
url = BASE_URL + profession_url
headers = {'User-Agent': ua.random}
results = {'Описание': [], 'Возраст': [], 'Место проживания': [], 'Ссылка': []}

# count how many pages listing has
response = requests.get(url, headers=headers)
soup = bs(response.text, 'html.parser')
nav_buttons = soup.find_all('a', class_='navi')
nav_buttons_count = len(nav_buttons)
if nav_buttons_count == 0:
    number_of_pages = 1
else:
    number_of_pages = nav_buttons_count - 1
print('Количество страниц в листинге:', number_of_pages)

# go through pages
for page in range(1, number_of_pages + 1):
    print(f'\nПарсинг страницы №{page}')
    response = requests.get(url + 'page' + str(page) + '.html', headers=headers)
    soup = bs(response.text, 'html.parser')
    ads = soup.find_all('a', class_='am')

    # go through ads on each page
    print('Объявления: ', end='')
    for ad in ads:
        print(ads.index(ad) + 1, end=' ')
        time.sleep(3)

        # --- Описание
        text = ad.text

        # --- Ссылка
        link = BASE_URL + ad.attrs['href']

        # follow link
        response = requests.get(link, headers=headers)
        soup = bs(response.text, 'html.parser')

        # --- Место проживания
        city = soup.find('td', id='tdo_1284')
        if not city is None:
            city = city.text

        # --- Возраст
        age = soup.find('td', id='tdo_56')
        if not age is None:
            age = age.text

        results['Описание'].append(text)
        results['Возраст'].append(age)
        results['Место проживания'].append(city)
        results['Ссылка'].append(link)

# write to Excel file
df = pd.DataFrame(results)
df['Ссылка'] = df.apply(lambda x: make_clickable(x['Ссылка'], 'Подробная информация'), axis=1)
file_name = 'список_объявлений' + '_' + PROFESSION + '.xlsx'
df.to_excel(file_name, sheet_name=PROFESSION, index=False)
print(f'\n\nПарсинг выполнен успешно. Количество объявлений: {len(results["Описание"])}')
print(f'Список объявлений находится в файле {file_name}')