import time
import csv
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

lst = ['Тип объявления', 'Вид объекта', 'Количество комнат', 'Тип дома', 'Площадь', 'Этаж', 'Цена', 'Ссылка']

with open('appartments.csv', 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(lst)

options = {'proxy': {
    'http': "socks5://XwkWNK:dEWz88@193.31.102.81:9234",
    'https': "socks5://XwkWNK:dEWz88@193.31.102.81:9234",
    }}

url = 'https://iv.kupiprodai.ru/realty/all_kvartiry/param803_813'

with webdriver.Chrome(seleniumwire_options=options) as browser:
    browser.get(url=url)
    time.sleep(15)
    for i in range(6):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    items = browser.find_element(By.TAG_NAME, 'ul').find_elements(By.TAG_NAME, 'li')
    apartments = []
    print('Добавляю стоимость и ссылки в список ...')
    for item in items:
        try:
            price = item.find_element(By.CLASS_NAME, 'list_price').text
            link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
            apartments.append([price, link])
        except:
            continue
    result = []
    mistakes = []
    print('Собираю информацию о квартирах ...')
    for i in range(len(apartments)):
        print(f'{i}/{len(apartments)}...')
        browser.get(apartments[i][1])
        time.sleep(1)
        des = [x.text.split()[-1] for x in browser.find_element(By.TAG_NAME, 'table').find_elements(By.TAG_NAME, 'tr')]
        try:
            result.append([des[0], des[1], des[2], des[3], des[4], f'{des[5]} из {des[6]}', apartments[i][0], apartments[i][1]])
        except:
            mistakes.append([*des, 'Ошибка: заполнены не все данные', apartments[i][0], apartments[i][1]])
    browser.quit()
with open('appartments.csv', 'a', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file, delimiter=';')
    for res in result:
        writer.writerow(res)
    for miss in mistakes:
        writer.writerow(miss)
print('Done')