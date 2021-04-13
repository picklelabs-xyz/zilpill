import src.utils.zil_utils as zutils
import math
import src.CONF as CONF
import time
import os
import src.CONSTANTS as CNSTS
from src.arb.zil import zilswap
import random
from pyzil.account import Account


api_url = zutils.set_zil_api()
zutils.set_env()

account = Account(private_key=zutils.get_key(os.getenv(CONF.PRIM_WALLET['KEYSTORE']),
                                             os.getenv(CONF.PRIM_WALLET['PASSWORD'])
                                             ))

zilswap_contract = zutils.load_contract(CNSTS.CONTRACT.ZIL_SWAP_CONTRACT_ADD, account)

token_of_interest_bech32 = CNSTS.TOKEN.ZCH_BECH32_ADD
min_zils_per_token = 28
token_bech32 = token_of_interest_bech32

initial_tokens = zutils.get_token_balance(token_bech32, zilswap_contract.account.bech32_address)
final_tokens = initial_tokens
liquidity_to_remove_per = 0.025/100

while final_tokens == initial_tokens:
    print("*"*100)
    print("min zils per token: ", min_zils_per_token)
    api_url = zutils.set_zil_api(api_url)
    code, msg = zilswap.limit_remove_liquidity(zilswap_contract,
                                               token_bech32,
                                               liquidity_to_remove_per,
                                               min_zils_per_token,
                                               gas_limit=CNSTS.ZLP_LP_REMOVE_GAS_LIMIT,
                                               gas_price=CNSTS.ZLP_AVG_GAS_PRICE
                                               )
    if code == "Fail":
        print(msg)
    else:
        final_tokens = zutils.get_token_balance(token_bech32, zilswap_contract.account.bech32_address)
    print("Taking a break for a min.")
    min_zils_per_token = random.randint(11, 14)
    time.sleep(2)
