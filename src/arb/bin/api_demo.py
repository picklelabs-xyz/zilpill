# https://github.com/binance/binance-spot-api-docs
# websocket to stream data continuously - websocket streams
# Base endpoint: wss://stream.binance.com:9443/


# wss://stream.binance.com:9443/ws/zilusdt@trade
# {"e":"trade","E":1613775690884,"s":"ZILUSDT","t":17447351,"p":"0.13607000","q":"3059.10000000","b":203290593,"a":203290625,"T":1613775690883,"m":true,"M":true}

# wscat -c wss://stream.binance.com:9443/ws/zilusdt@kline_5m
# kline: {"e":"kline","E":1613775963782,"s":"ZILUSDT","k":{"t":1613775900000,"T":1613776199999,"s":"ZILUSDT","i":"5m","f":17447515,"L":17447596,"o":"0.13642000","c":"0.13681000","h":"0.13695000","l":"0.13642000","v":"197011.10000000","n":82,"x":false,"q":"26929.17201400","V":"151068.50000000","Q":"20654.40785300","B":"0"}}
# OHLC data, open high, low, close

# wscat -c wss://stream.binance.com:9443/ws/zilusdt@kline_5m | tee dataset.txt


# https://github.com/tradingview/lightweight-charts

# cdn: https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js

# https://python-binance.readthedocs.io/en/latest/

import src.CONSTANTS as CNSTS
import os
import src.CONF as CONF
import json
from src.stk import zillion
from src.utils import email_info
from datetime import datetime
from dotenv import load_dotenv
from binance.client import Client
import csv

load_dotenv()
personal_env = os.getenv(CONF.PERSONAL_ENV_FILE)
load_dotenv(personal_env)

api_key = os.getenv(CONF.BIN_WALLET_1_API_1["API_KEY"])
api_secret = os.getenv(CONF.BIN_WALLET_1_API_1["API_SECRET"])

client = Client(api_key, api_secret)

# candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_30MINUTE)
candles = client.get_historical_klines('ZILUSDT',
                                       Client.KLINE_INTERVAL_15MINUTE,
                                       '5 Mar, 2018',
                                       '20 Feb, 2021'
                                       )

csv_data_file = open("../../../data/bin/zil_btc_kline_15.csv", "w", newline='')
csv_data_writer = csv.writer(csv_data_file, delimiter=',')

print(len(candles))
csv_data_writer.writerows(candles)
print(candles[0])

csv_data_file.close()

