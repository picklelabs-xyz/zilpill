import os
import sys
import src.CONSTANTS as CNSTS
import os
import src.CONF as CONF
import json
import math
from src.stk import zillion
from src.utils import email_info
from datetime import datetime
from dotenv import load_dotenv
from binance.client import Client
import csv
import talib


def get_binance_data():
    load_dotenv()
    personal_env = os.getenv(CONF.PERSONAL_ENV_FILE)
    load_dotenv(personal_env)

    api_key = os.getenv(CONF.BIN_WALLET_1_API_1["API_KEY"])
    api_secret = os.getenv(CONF.BIN_WALLET_1_API_1["API_SECRET"])

    client = Client(api_key, api_secret)

    start_date = "5 Feb, 2021"
    end_date = "20 Feb, 2021"
    asset_pair = 'ZILUSDT'
    data_type = "kline_15m"

    # candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_30MINUTE)
    candles = client.get_historical_klines(asset_pair,
                                           Client.KLINE_INTERVAL_15MINUTE,
                                           start_date,
                                           end_date
                                           )
    return candles


# if asset1 changes by delta_asset1 %, and asset2 changes by delta_asset2 %, then calculate new relative price
def get_updated_price(asset_price_in_usd, asset_price_delta):
    return asset_price_in_usd * (1 + asset_price_delta)


def get_current_total_worth(asset1_amount, asset1_price, asset2_amount, asset2_price):
    return asset1_amount * asset1_price + asset2_amount * asset2_price


def get_pool_asset_amounts(asset1_amount,
                           asset2_amount,
                           updated_asset1_rel_price_to_asset2):
    asset1_rel_price_to_asset2 = asset2_amount/asset1_amount
    print(asset1_rel_price_to_asset2)
    constant_product = asset1_amount * asset2_amount
    asset1_updated_amount = math.sqrt((asset1_rel_price_to_asset2/updated_asset1_rel_price_to_asset2)
                                     * asset1_amount * asset1_amount)
    asset2_updated_amount = constant_product/asset1_updated_amount
    return asset1_updated_amount, asset2_updated_amount


asset1_pool_target_weight = 0.5
asset2_pool_target_weight = 0.5

# asset1_borrow_rate = 5 # Rate of borrowing an asset from a centralized exchange or a smart contract etc.
# asset2_borrow_rate = 10
# asset1_liquidity_range_constraint = 5 # Percentage change in liquidity +- both, can be separated as well

asset1_price_in_usd = 0.17
asset2_price_in_usd = 1

asset1_rel_price_in_asset2 = asset1_price_in_usd/asset2_price_in_usd

user_invested_amount_in_usd = 100000

asset1_price_delta = 0.248 # In percentage
asset1_updated_price = get_updated_price(asset1_price_in_usd, asset1_price_delta)

asset2_price_delta = 0.0 # In percentage
asset2_updated_price = get_updated_price(asset2_price_in_usd, asset2_price_delta)

asset1_updated_rel_price_in_asset2 = asset1_updated_price/asset2_updated_price

# assuming a delta of 1-5% change in reaching the target price change in asset 1

user_asset1_initial_amount = (user_invested_amount_in_usd * asset1_pool_target_weight) / asset1_price_in_usd
user_asset2_initial_amount = (user_invested_amount_in_usd * asset2_pool_target_weight) / asset2_price_in_usd

print("Initial worth", get_current_total_worth(user_asset1_initial_amount, asset1_price_in_usd,
                                               user_asset2_initial_amount, asset2_price_in_usd))

# To ignore slippage for the simulation, assume a very high amount of liquidity in the select pool
asset_pool_liquidity_multiplier = 1000
pool_asset1_initial_amount = user_asset1_initial_amount * asset_pool_liquidity_multiplier
pool_asset2_initial_amount = user_asset2_initial_amount * asset_pool_liquidity_multiplier

print("zil initial: ", asset1_rel_price_in_asset2)
print("zil updated: ", asset1_updated_rel_price_in_asset2)

pool_asset1_updated_amount, pool_asset2_updated_amount = get_pool_asset_amounts(pool_asset1_initial_amount,
                                                                                pool_asset2_initial_amount,
                                                                                asset1_updated_rel_price_in_asset2)
user_asset1_updated_amount = pool_asset1_updated_amount/asset_pool_liquidity_multiplier
user_asset2_updated_amount = pool_asset2_updated_amount/asset_pool_liquidity_multiplier


print("zil: ", user_asset1_initial_amount)
print("usd: ", user_asset2_initial_amount)
print("zil change: ", asset1_price_delta * 100, " %")
print("zil: ", user_asset1_updated_amount)
print("usd: ", user_asset2_updated_amount)

current_worth = get_current_total_worth(user_asset1_updated_amount, asset1_updated_price,
                        user_asset2_updated_amount, asset2_updated_price)
print("Current worth", current_worth)

hold_strategy_worth = get_current_total_worth(user_asset1_initial_amount, asset1_updated_price,
                                                     user_asset2_initial_amount, asset2_updated_price)
print("Hold strategy worth", hold_strategy_worth)
impermanent_loss = round(((current_worth-hold_strategy_worth)/hold_strategy_worth) * 100, 2)
print("Impermanent loss: ", impermanent_loss)

print("Asset 1 % change: ", round(((user_asset1_updated_amount - user_asset1_initial_amount)/user_asset1_initial_amount)*100, 2))