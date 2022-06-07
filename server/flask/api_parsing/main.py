
from argparse import Action
import datetime
from http.client import HTTPConnection
import json
from typing import List
from warnings import catch_warnings
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import sys
import os
# Добавляю в pythonpath так, чтобы не портить глобальное значение
sys.path.append(os.path.expanduser('~/Documents/snakelizator/server/flask/'))
# print(sys.path)

from db.main import insert_data


def parse_data(minutes: float) -> List[object]:
    try:
        area = 1563
        headers = {"User-Agent": "snakelizator"}
        conn = HTTPConnection("api.hh.ru")
        per_page = 100
        page = 0
        date_from = (datetime.datetime.now() - datetime.timedelta(minutes=minutes)).strftime('%Y-%m-%dT%H:%M:%S')
        date_to = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        path = f"/vacancies?per_page={per_page}&page={page}&area={area}&date_from={date_from}&date_to={date_to}"
        print("Request to api.hh.ru" + path)

        with webdriver.Firefox() as driver:
            # Open URL
            driver.get("https://api.hh.ru"+path)
            resp = driver.find_element(By.ID, "json")
            resp = resp.text
        
        count = insert_data(json.loads(resp))
        if count == 0: count = -1

    except: return -1, []
    return count, json.loads(resp)




# insert_data(json.loads(resp)) 

# area = 1563
# headers = {"User-Agent": "snakelizator"}
# conn = HTTPConnection("api.hh.ru")
# per_page = 100
# page = 0
# date_from = (datetime.datetime.now() - datetime.timedelta(minutes=260)).strftime('%Y-%m-%dT%H:%M:%S')
# date_to = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
# path = f"/vacancies?per_page={per_page}&page={page}&area={area}&date_from={date_from}&date_to={date_to}"
# print("Request to api.hh.ru" + path)

# with webdriver.Firefox() as driver:
#     # Open URL
#     driver.get("https://api.hh.ru"+path)
#     resp = driver.find_element(By.ID, "json")
#     resp = resp.text


# insert_data(json.loads(resp))

