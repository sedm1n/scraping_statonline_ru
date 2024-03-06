import os
import requests
import time

def get_respounde(url):
    try:
        response = requests.get(url)
        time.sleep(4)
        response.raise_for_status()  # Проверка статуса ответа
    except requests.exceptions.RequestException as e:

        if isinstance(e, requests.exceptions.ConnectionError):
           return True
        elif isinstance(e, requests.exceptions.Timeout):
            return False
        else:
            return False
    else:
        return False

def chekdomen():
    list_files = os.listdir(os.curdir+'/data/domens')
    list_domens = []
    good_domen = []
    bad_domen = []
    for file in list_files:
        with open(f"data/domens/{file}", 'r') as file_domen:
            list_domens = file_domen.readlines()

    for link in list_domens:
        print(f"Проверяем {link.strip()}")
        if get_respounde(link):
            with open('data/good.txt','a') as file_good:
                file_good.write(f"{link.strip()}\n")
        else:
            bad_domen.append(link)


chekdomen()

