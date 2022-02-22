from data_populate import config
import csv
import psycopg2.extras
import re

connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
cursor.execute("select * from stock where symbol in ('ARKF', 'ARKG', 'ARKK', 'ARKQ', 'ARKW', 'IZRL', 'PRNT');")
etfs = cursor.fetchall()

dates = ['2022-02-21']

for current_date in dates:
    for etf in etfs:
        print(etf['symbol'])

        with open(f"etfdata/{current_date}/{etf['symbol']}.csv") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if len(row) < 8:
                    print(f'Cant process ROW: {row}')
                    continue
                ticker = row[3]
                if ticker:
                    shares = ''.join([i for i in row[5] if i.isdigit()])
                    weight = re.sub(r"%", "", row[7])

                    cursor.execute("""
                        SELECT * FROM stock WHERE symbol = %s
                    """, (ticker,))
                    stock = cursor.fetchone()
                    if stock:
                        cursor.execute("""
                            INSERT INTO etf_holding (etf_id, holding_id, dt, shares, weight)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (etf['id'], stock['id'], current_date, shares, weight))

connection.commit()