import json
from pprint import pprint
from symtable import SymbolTableFactory
from unicodedata import name
import yaml
import redis

with open('../redis/config.yml', 'r') as file:
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
        
# insert_test_data()
print(r.dbsize())

# поля для анализа: 
#     name
#     salary
#     schedule
#     snippet
