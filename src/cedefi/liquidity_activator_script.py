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


# 1. Following constant product formula for market making, x * y = k
# 2. where, x is the amount of asset 1, and y is the amount of asset 2 pooled in.
# 3. Assuming price of asset 1 in relation to asset 2 is m, 
# 4. then y = m * x, therefore k = x * m * x 
# 5. Considering a change in relative price of asset 1 to asset 2 i.e. m -> m',
# 6. Updated state of pooled assets x -> x', y-> y'
# 7. x' * m' * x' = k, therefore x' * m' * x' = x * m * x
# 8. x' = sqr_rt((x * m * x)/m')
# 9. Assuming m' = n * m, where it can be read as new relative price of asset 1 is n% of the current price
# 10. x' = sqr_rt((x * x)/n) 
# 11. y' = k/x'
# 12. Lets consider the $ value of asset 2 unit as v, asset 1 unit $ value (u) would be v * m
# 13. Therefore, total worth of the assets would be x * (v * m) + y * v  
# 14. Considering the updated $ value of asset 2 as u'
# 15. Difference in assets worth would be: (x' * (u' * m') + y' * u') - (x * (u * m) + y * u) 
# 16. This difference is referred to as impermanent loss i.e. comparing the buy and hold strategy vs putting assets in the pool

# Experiment with different price curves,
# e.g. assuming a delta of 1-5% change in reaching the target price change in the assets

def get_updated_price(price, price_delta):
    return price * (1 + price_delta)

def k(x, y):
    return x * y

def worth(x, u, y, v):
    return x * u + y * v

def worth_with_m(x, y, v, m):
    return x * (v * m) + y * v

def get_updated_x_y(x, y, m_dash):
    m = y/x
    product = k(x,y)
    x_dash = math.sqrt((m/m_dash) * x * x)
    y_dash = product/x_dash
    return x_dash, y_dash


a1_pool_weight = 0.5
a2_pool_weight = 0.5
a1_borrow_rate = 5 # Rate of borrowing an asset from a centralized exchange or a smart contract etc.
a2_borrow_rate = 10
# asset1_constraint_range = 5 # Percentage change in liquidity +- both, can be separated as well

# Assuming following, user pool in: 10K $, zil at 0.17$, Zil-USD pool
# change of 50% price in Zil
# Goal is to maximize time stayed in the pool, while minimizing the impermanent loss

# Assume asset 1 as x, and asset 2 as y following the above formulation
u = 0.17 # $ price of asset 1
v = 1 # $ price of asset 2
m = u/v
delta_u = 0.5 # Percent change
u_dash = get_updated_price(u, delta_u)
delta_v = 0.0 # Percent change
v_dash = get_updated_price(v, delta_v)
m_dash = u_dash/v_dash

user_amount_in_usd = 10000
user_x = (user_amount_in_usd * a1_pool_weight) / u
user_y = (user_amount_in_usd * a2_pool_weight) / v
print("user x: ", user_x, " user y: ", user_y)
user_worth = worth(user_x, u, user_y, v)
print("Initial user worth", user_worth)

# To ignore slippage for the simulation, assume a very high amount of liquidity in the select pool
# Assuming a high asset1-asset2 dex pool, i.e. <0.1% slippage for any invested amount
pool_approx_liq_multiplier = 1000
pool_x = user_x * pool_approx_liq_multiplier
pool_y = user_y * pool_approx_liq_multiplier
print("pool x: ", pool_x, " pool y: ", pool_y)

pool_x_dash, pool_y_dash = get_updated_x_y(pool_x, pool_y, m_dash)
print("pool x: ", pool_x_dash, " pool y: ", pool_y_dash)

user_x_dash = pool_x_dash / pool_approx_liq_multiplier
user_y_dash = pool_y_dash / pool_approx_liq_multiplier
print("user x: ", user_x_dash, " user y: ", user_y_dash)
user_updated_worth = worth(user_x_dash, u_dash, user_y_dash, v_dash)
print("Updated user worth", user_updated_worth)

print("Asset 1 price with ", round(delta_u*100, 2), " % change:" , u, " -> ", u_dash)
print("Asset 2 price with ", round(delta_v*100, 2), " % change:" , v, " -> ", v_dash)

user_buy_hold_worth = worth(user_x, u_dash, user_y, v_dash)
il = (user_updated_worth - user_buy_hold_worth)/user_buy_hold_worth
print("Impermanent loss %: ", round(il, 2))
print("User buy and hold worth: ", round(user_buy_hold_worth, 2))

print("Asset 1 % change: ", round(((user_x_dash - user_x)/user_x)*100, 2))
print("Asset 2 % change: ", round(((user_y_dash - user_y)/user_y)*100, 2))