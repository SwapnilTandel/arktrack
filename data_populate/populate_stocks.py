from data_populate import config
import json
import psycopg2.extras
import requests

connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
print(f'API_SECRET: %s', config.API_SECRET)
print(f'IEX_TOKEN: %s', config.IEX_TOKEN)
if config.IEX_TOKEN:
    resp = requests.get(f'https://cloud.iexapis.com/stable/ref-data/symbols?token={config.IEX_TOKEN}')
    response = json.loads(resp.content)

    for asset in response:
        print(f"Inserting stock {asset['name']} {asset['symbol']}")
        cursor.execute("""
            INSERT INTO stock (symbol, name, exchange, is_etf, type, is_enable, region, figi)
            VALUES (%s, %s, %s, false, %s, %s, %s, %s)
        """, (asset['symbol'], asset['name'], asset['exchange'], asset['type'], asset['isEnabled'],
              asset['region'], asset['figi']))

connection.commit()
