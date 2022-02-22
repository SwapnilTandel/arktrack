import os

DB_HOST = '127.0.0.1'
DB_NAME = os.getenv('TIMESC_DB')
DB_USER = os.getenv('TIMESC_U')
DB_PASS = os.getenv('TIMESC_P')

APCA_API_URL = 'https://paper-api.alpaca.markets'
APCA_API_KEY = os.getenv('APCA_API_KEY_ID')
APCA_API_SECRET = os.getenv('APCA_API_SECRET_KEY')

IEX_TOKEN = os.getenv('IEXP_API')

POLY_API_KEY = os.getenv('POLY_API_KEY')
