
import datetime
from http.client import HTTPConnection
import json


area = 1563
headers = {"User-Agent": "snakelizator"}
conn = HTTPConnection("api.hh.ru")
per_page = 100
page = 0
date_from = (datetime.datetime.now() - datetime.timedelta(minutes=120)).strftime('%Y-%m-%dT%H:%M:%S')
date_to = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
path = f"/vacancies?per_page={per_page}&page={page}&area={area}&date_from={date_from}&date_to={date_to}"
print("Request to api.hh.ru" + path)
conn.request("GET", path, headers=headers)
resp = conn.getresponse()
print(f"Status: {resp.status}")
if resp.status == 200:
    vacancies = resp.read()
    print(json.loads(vacancies))
conn.close()
