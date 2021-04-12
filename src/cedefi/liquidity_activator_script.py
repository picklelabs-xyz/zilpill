import src.CONSTANTS as CNSTS
import os
import src.CONF as CONF
import json
import math
import csv
import talib
import numpy as np
import pandas as pd
import plotly.express as px
from src.stk import zillion
from src.utils import email_info
from datetime import datetime
from dotenv import load_dotenv
from binance.client import Client

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

# what 1 transaction would bring a change of price of x% in asset1 in the pool
# a buy order of asset1 would increase the price, while a sell order decreases the price
# calculate the amount of asset1 tokens need to be bought from this pool to
# increase asset1 price by x%
# Assuming a high asset1-asset2 dex pool, i.e. <1% slippage for any invested amount
# roi through liquidity mining is defined by the time spent by the liquidity spent in the pool, which in turn
# gives the amount of fees earned and the governance token rewards
# track binance price continuously, if it changes by 2%, then remove the liquidity
# also note that there could be a lag between the binance prices and the dex price or vice versa (in some cases)
# leading to arbitrage opportunities

# TODO Classes: DexPool, Asset

def load_env():
    load_dotenv()
    personal_env = os.getenv(CONF.PERSONAL_ENV_FILE)
    load_dotenv(personal_env)

load_env()


class ConstantProductPool:
    x = 0
    y = 0
    u = 0
    v = 0
    m = 0

    a1_pool_weight = 0.5
    a2_pool_weight = 0.5

    def __init__(self, u, v, w):
        self.u = u
        self.x = (w * a1_pool_weight) / self.u
        self.v = v
        self.y = (w * a2_pool_weight) / self.v
        self.m = u / v

    def current_state(self):
        return self.x, self.yy

    def product(self, x, y):
        return self.x * self.y

    def worth(self):
        return self.x * self.u + self.y * self.v

    def update(self, u_dash, v_dash):
        m_dash = u_dash / v_dash
        k = self.product(self.x, self.y)
        self.x = math.sqrt((self.m / m_dash) * self.x * self.x)
        self.y = k / self.x
        self.u = u_dash
        self.v = v_dash
        self.m = m_dash

    def get_user_current_state(self, user_share):
        return user_share * self.x, user_share * self.y

    def get_user_worth(self, user_share):
        return user_share * self.worth()


def get_updated_price(price, price_delta):
    return price * (1 + price_delta)

def worth(x, u, y, v):
    return x * u + y * v


# Example IL calculation
a1_pool_weight = 0.5
a2_pool_weight = 0.5

# Assuming following, user pool in: 10K $, zil at 0.17$, Zil-USD pool
# change of 50% price in Zil

u = 0.17 # $ price of asset 1
v = 1 # $ price of asset 2
delta_u = 0.5 # Percent change
delta_v = 0.0 # Percent change
pool_initial_worth = 1000000000
pool = ConstantProductPool(u, v, pool_initial_worth)
user_initial_worth = 10000
user_share = user_initial_worth/pool_initial_worth
user_x, user_y = pool.get_user_current_state(user_share)
print("Initial user worth", pool.get_user_worth(user_share))
print("user x: ", user_x, " user y: ", user_y)
u_dash = get_updated_price(u, delta_u)
v_dash = get_updated_price(v, delta_v)
pool.update(u_dash, v_dash)
user_x_dash, user_y_dash = pool.get_user_current_state(user_share)
print("user x: ", user_x_dash, " user y: ", user_y_dash)
print("Updated user worth", pool.get_user_worth(user_share))
user_buy_hold_worth = worth(user_x, u_dash, user_y, v_dash)
il = (pool.get_user_worth(user_share) - user_buy_hold_worth)/user_buy_hold_worth
print("Impermanent loss %: ", round(il * 100, 2))
print("User buy and hold worth: ", round(user_buy_hold_worth, 2))
print("Asset 1 % change: ", round(((user_x_dash - user_x)/user_x)*100, 2))
print("Asset 2 % change: ", round(((user_y_dash - user_y)/user_y)*100, 2))


def get_binance_client():
    api_key = os.getenv(CONF.BIN_WALLET_1_API_1["API_KEY"])
    api_secret = os.getenv(CONF.BIN_WALLET_1_API_1["API_SECRET"])
    client = Client(api_key, api_secret)
    return client


def get_binance_data(client, start_date, end_date, asset_pair, data_type):
    candles = client.get_historical_klines(asset_pair,
                                           Client.KLINE_INTERVAL_15MINUTE,
                                           start_date,
                                           end_date
                                           )
    return candles


def candles_to_df(candles):
    rows_list = []
    for candle in candles:
        row_dict = {}
        row_dict['Open time'] = candle[0]
        row_dict['Open'] = candle[1]
        row_dict['High'] = candle[2]
        row_dict['Low'] = candle[3]
        row_dict['Close'] = candle[4]
        row_dict['Volume'] = candle[5]
        row_dict['Close time'] = candle[6]
        row_dict['Quote asset volume'] = candle[7]
        row_dict['Number of trades'] = candle[8]
        row_dict['Taker buy base asset volume'] = candle[9]
        row_dict['Taker buy quote asset volume'] = candle[10]
        row_dict['Can be ignored'] = candle[11]

        rows_list.append(row_dict)

    df = pd.DataFrame(rows_list)
    return df


start_date = "5 Feb, 2021"
end_date = "20 Feb, 2021"
asset_pair = 'ZILUSDT'
data_type = "kline_15m"
client = get_binance_client()
candles = get_binance_data(client, start_date, end_date, asset_pair, data_type)
candles = candles_to_df(candles)
candles['Open time stamp'] = candles.apply(lambda x: datetime.fromtimestamp(x["Open time"]/1000.0),axis=1)
candles['Close'] = candles['Close'].astype(float)


total_time = 0
time_spent_in_pool =  0
# To start with, asset 1 is speculative, and asset 2 is a stable one (FIAT).
# Idea is to maximize time spent by the liquidity in the pool, while minimizing the
# change in the percentage of the asset 1.
# With any of the implemented approaches, aim is to beat the losses (asset 1 loss and/or IL)
# occuring with doing no dynamic liquidity additions/removals.
# Approach 1: Put a constraint on the change of asset 1 %, and remove liquidity if the change
# is more than the threshold.

u = candles.iloc[0]['Close']
v = 1
pool_initial_worth = 100000000
pool = ConstantProductPool(u, v, pool_initial_worth)
user_initial_worth = 10000
user_share = user_initial_worth/pool_initial_worth
ils = []

u_losses = []
u_start_delta = []
u_recent = u
user_x, user_y = pool.get_user_current_state(user_share)
for index, row in candles.iterrows():
    u_dash = row['Close']
    v_dash = v
    pool.update(u_dash, v_dash)
    user_x_dash, user_y_dash = pool.get_user_current_state(user_share)
    user_buy_hold_worth = worth(user_x, u_dash, user_y, v_dash)
    il = (pool.get_user_worth(user_share) - user_buy_hold_worth)/user_buy_hold_worth
    ils.append(round(il * 100, 2))
    u_losses.append(round(((user_x_dash - user_x)/user_x)*100, 2))

print(ils[len(ils)-1])
print(u_losses[len(u_losses)-1])
result = pd.DataFrame({"IL": ils, "Asset1_Loss": u_losses})
print(result.head(5))


