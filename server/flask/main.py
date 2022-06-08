from crypt import methods
import datetime
import sys
import os
# Добавляю в pythonpath так, чтобы не портить глобальное значение
sys.path.append(os.path.expanduser('~/Documents/snakelizator/server/flask/'))

from flask import Flask
from flask import jsonify
from flask import request
from db.main import collect_data, insert_data, count_mid_salary
from api_parsing.main import parse_data

app = Flask(__name__)

@app.route('/')
def hello_world():
    return """
     <textarea style="  width: 100%; height: 100%; resize: none; border: none; background: black; color: white; margin: 0; padding: 0;">
        .---. .-. .-.  .--.  ,-. .-.,---.  ,-.    ,-. _____    .--.  _______  .---.  ,---.    
       ( .-._)|  \| | / /\ \ | |/ / | .-'  | |    |(|/___  /  / /\ \|__   __|/ .-. ) | .-.\   
      (_) \   |   | |/ /__\ \| | /  | `-.  | |    (_)   / /) / /__\ \ )| |   | | |(_)| `-'/   
      _  \ \  | |\  ||  __  || | \  | .-'  | |    | |  / /(_)|  __  |(_) |   | | | | |   (    
     ( `-'  ) | | |)|| |  |)|| |) \ |  `--.| `--. | | / /___ | |  |)|  | |   \ `-' / | |\ \   
      `----'  /(  (_)|_|  (_)|((_)-'/( __.'|( __.'`-'(_____/ |_|  (_)  `-'    )---'  |_| \)\  
             (__)            (_)   (__)    (_)                               (_)         (__) 
     </textarea>
    """

@app.route('/raw')
def return_raw_data():
    resp = collect_data()
    if len(resp) != 0:
        app.logger.info(f'Returned {len(resp)} vacancies')
        return{
            "Status": "ok",
            "rows": len(resp),
            "data": resp
        }
    else:
        app.logger.info(f'Returned 0 vacancies')
        return{
            "Status": "error",
            "rows": 0,
            "data": []
        }

@app.route('/collect')
def collect_data_from():
    minutes = int(request.args.get('minutes'))
    app.logger.info(f'Started parsing data from {datetime.datetime.now()-datetime.timedelta(minutes=minutes)} until now')
    count, resp = parse_data(minutes)
    count = int(count)
    if count != -1:
        app.logger.info(f'Added {count} rows into database')
        return {
            'Status': 'ok',
            'rows': count,
            'data': resp
        }
    else:
        app.logger.info(f'Ups, something went wrong!')
        return {
            'Status': 'error',
            'rows': 0,
            'data': []
        }

@app.route('/salary')
def return_mid_salary():
    resp = count_mid_salary()
    return{
        "Status": "ok",
        "mid_salary": resp
    }

if __name__ == '__main__':
    app.run()