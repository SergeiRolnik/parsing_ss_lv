from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

URL = 'https://www.ss.lv/ru/work/i-search-for-work/collector/'
CHROME_WEBDRIVER_LOCATION = 'driver/chromedriver.exe'
driver = webdriver.Chrome(CHROME_WEBDRIVER_LOCATION)
driver.get(URL)
# driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")

link = driver.find_element(By.XPATH, '//*[@id="dm_47533426"]')
link_text = link.text
link_href = link.get_attribute('href')
print('Ссылка:', link_text, link_href)
link.click()

age = driver.find_element(By.ID, 'tdo_56')
age_text = age.text

city = driver.find_element(By.ID, 'tdo_1284')
city_text = city.text

print('Возраст:', age_text)
print('Город:', city_text)

with open('../ads.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow([link_text, age_text, city_text, link_href])

driver.close()