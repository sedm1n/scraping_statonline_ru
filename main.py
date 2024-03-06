import requests
from PIL import Image
from fake_useragent import UserAgent
import time
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from twocaptcha import TwoCaptcha
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pickle
import re
import os
from chekdomens import chekdomen
from parse_domens import parse_pages
from settings import API_KEY

# Option
option = webdriver.ChromeOptions()
user_agent = UserAgent()
# proxy_options = {
#    'proxy': {
#       'https':f"https://{login}:{password}@1,1,1.2"
#    }
# }
option.add_argument(f"user-agent={user_agent.random}:")


def chek_captcha(driver):
    try:
        ele_captcha = driver.find_element(By.XPATH, "//img[@alt='CAPTCHA']")
        src = ele_captcha.get_attribute('src')
        img_captcha = ele_captcha.screenshot_as_png

        with open('captcha.jpg', 'wb') as f:
            f.write(img_captcha)

        return True
    except NoSuchElementException:
        return False

def save_pages(driver):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    page_num = soup.find('div', class_='paginator').find_all('span')[-1].text
    while chek_captcha(driver):
        captcha_solving(driver)

    for page in range(1, int(page_num)):
        url = f"https://statonline.ru/domains?rows_per_page=100&page={page}&tld=ru&order=ASC&dns=ns1%2Efirstvds%2Eru"
        driver.get(url)
        source = driver.page_source
        time.sleep(4)
        with open(f'data/pages/page{page}.html', 'w') as file_page:
            file_page.write(source)


def captcha_solving(driver):
    solver = TwoCaptcha(API_KEY)
    result = solver.normal('captcha.jpg')

    captcha_input = driver.find_element(By.NAME, 'captcha')
    print( captcha_input)
    time.sleep(3)
    captcha_input.send_keys(result['code'].upper())
    time.sleep(3)
    driver.find_element(By.XPATH, '//button[@class="button-20 button-green"]').click()
    print('otpravil captcha')
    time.sleep(4)
def main():
    ans = input(""" Выберите вариант:
        1) Парсим страницы с доменами
        2) Проверяем домены на валидность
     """)
    if ans == '1':
        show_window = input("Показыать окно браузера 1 или 0")
        if show_window == "0":
            option.add_argument("--headless=new")
        print("Запускаем парсинг доменов")

        url = 'https://statonline.ru/domains?rows_per_page=100&page=1&tld=ru&order=ASC&dns=ns1%2Efirstvds%2Eru&sort_field=domain_name_idn'
        driver = webdriver.Chrome(options=option)

        try:
            driver.get(url)

            for cookie in pickle.load(open('session', 'rb')):
                driver.add_cookie(cookie)

            driver.refresh()

            while chek_captcha(driver):
                captcha_solving(driver)

            pickle.dump(driver.get_cookies(), open('session', 'wb'))
            save_pages(driver)
            parse_pages()


        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()
    elif ans == '2':
        print("Запускаем проверку доменов")
        chekdomen()



if __name__ == '__main__':
    main()
