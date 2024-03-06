from bs4 import BeautifulSoup
import os
import re
def scrap_page(src):
    soup = BeautifulSoup(src, 'lxml')
    all_domens = soup.find_all('td', class_='b')
    list_domen = []
    pattern = r'domain=([^&"]+)'
    for domen in all_domens:
        dm = re.search(pattern, str(domen.find('a')))
        if dm:
            list_domen.append(dm.group(1))

    with open('data/domens/domens.txt', 'a') as file_domens:
        for domen in list_domen:
            file_domens.write(f"{domen}\n")


def parse_pages():
    """
    Функция парсит домены с сохраненных страниц

    """
    list_pages = os.listdir(os.curdir + '/data/pages')
    for page in list_pages:
        with open(f"data/pages/{page}", 'r') as file:
            src = file.read()
        scrap_page(src)



