import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import json

professions_urls = {}
ua = UserAgent()
URL = 'https://www.ss.lv/ru/work/i-search-for-work/handyman/'
headers = {'User-Agent': ua.random}

response = requests.get(URL, headers=headers)
soup = bs(response.text, 'html.parser')
professions = soup.find(lambda tag: tag.name == 'select' and tag.get('class') == ['filter_sel']).find_all('option')

for profession in professions:
    profession_name = profession.text
    profession_url = profession.attrs['value']
    professions_urls[profession_name] = profession_url

file = open('professions.json', 'w', encoding='utf-8')
json.dump(professions_urls, file, ensure_ascii=False, indent=0)
file.close()
print('Парсинг выполнен успешно. Список специальностей находится в файле professions.json')