import json
from pprint import pprint
from symtable import SymbolTableFactory
from types import NoneType
from unicodedata import name
import yaml
import redis
import os

with open(os.path.abspath('db/config.yml'), 'r') as file:
    db_settings = yaml.safe_load(file)

r = redis.Redis(host=db_settings['host'], port=db_settings['port'])



def insert_test_data():
    with open('../test/test.json', 'r') as file:
        vacancies = json.load(file)
        pprint(vacancies['items'][0])
    with r.pipeline() as pipe:
        for temp in vacancies['items']:
            print(temp['id'])
            pipe.mset({temp['id']: json.dumps(temp)})
        pipe.execute()

def insert_data(data: str) -> int:
    with r.pipeline() as pipe:
        i = 0
        for temp in data['items']:
            print(temp['id'])
            pipe.mset({temp['id']: json.dumps(temp)})
            i += 1
        pipe.execute()
    return i

def collect_data() -> list:
    data = []
    keys = r.keys()
    for t in keys:
        temp_str = r.mget(t)[0].decode('utf8')
        data.append(json.loads(temp_str))
    return data

def count_mid_salary() -> float:
    data = []
    keys = r.keys()
    mid = 0
    for t in keys:
        temp_str = r.mget(t)[0].decode('utf8')
        data.append(json.loads(temp_str))
        if json.loads(temp_str)['salary'] != None:
            if json.loads(temp_str)['salary']['from']!= None:
                mid += json.loads(temp_str)['salary']['from']
    mid /= len(keys)
    return mid




# insert_test_data()
# print(r.dbsize())

# поля для анализа: 
#     name
#     salary
#     schedule
#     snippet



#TODO: 2Fish
