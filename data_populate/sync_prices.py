from data_populate import config
import psycopg2.extras
import logging
from os.path import exists
import requests
import json
import time
import datetime

LOG_FILE = '../etfdata/log_me.txt'
''' INIT '''
if exists(LOG_FILE):
    lfile = open(LOG_FILE, "w+")
    lfile.truncate()
    lfile.close()

logging.basicConfig(filename=LOG_FILE, filemode='a', level=logging.ERROR)
logger = logging.getLogger(__name__)

connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


def get_all_stocks(start_date, end_date):
    rtn_stocks = []
    cursor.execute(f"SELECT id, symbol FROM stock WHERE id IN (SELECT holding_id FROM etf_holding)")
    stocks = cursor.fetchall()

    for stock in stocks:
        cursor.execute(f"SELECT * FROM stock_price WHERE stock_id={stock['id']} and date(dt) between '"
                       f"{start_date}' and '{end_date}' limit 1;")
        if 0 == cursor.rowcount:
            rtn_stocks.append((stock['symbol'], stock['id']))
    return rtn_stocks


def load_data(symb, stock_id, start_date, end_date):
    url_q = f"https://api.polygon.io/v2/aggs/ticker/{symb}" \
            f"/range/1/minute/{start_date}/{end_date}?limit=120&apiKey={config.POLY_API_KEY}"
    resp = requests.get(url_q)
    response = json.loads(resp.content)
    if not response:
        # print(f'Response is empty for {symb}')
        logger.error(f'{symb}::Failed to fetch data.')
        return
    print(f'Data INSERT for {symb}')

    for bar in response.get('results', []):
        _d = (stock_id, datetime.datetime.fromtimestamp(bar['t'] / 1000.0), round(bar['o'], 2),
                round(bar['h'], 2), round(bar['l'], 2), round(bar['c'], 2), bar['v'])
        cursor.execute("""
            INSERT INTO stock_price (stock_id, dt, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, _d)
    connection.commit()

    print(f'Data COMMIT for {symb}')
    time.sleep(15)


def main():
    start_date, end_date = '2022-02-15', '2022-02-17'
    to_query = get_all_stocks(start_date, end_date)

    for sym, id in to_query:
        load_data(sym, id, '2022-02-15', '2022-02-17')


main()
