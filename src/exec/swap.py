import src.utils.zil_utils as zutils
import math
import src.CONF as CONF
import time
import os
import src.CONSTANTS as CNSTS
from src.arb.zil import zilswap
import random
from pyzil.account import Account
from dotenv import load_dotenv
from pyzil.zilliqa import chain


def set_zil_api(last_api_url):
    api_url = zutils.get_zil_api_url()
    while last_api_url==api_url:
        api_url = zutils.get_zil_api_url()
    print(api_url)
    vMainNet = chain.BlockChain(api_url, version=65537, network_id=1)
    chain.set_active_chain(vMainNet)
    return api_url

def set_env():
    load_dotenv()
    personal_env = os.getenv(CONF.PERSONAL_ENV_FILE)
    load_dotenv(personal_env)

api_url = set_zil_api(CNSTS.ZILLIQA_API_URL)
set_env()

tokens_of_interest = {"ZCH": CNSTS.TOKEN.ZCH_BECH32_ADD,
                      "XSGD": CNSTS.TOKEN.XSGD_BECH32_ADD,
                      "ZWAP": CNSTS.TOKEN.ZWAP_BECH32_ADD,
                      "CARB": CNSTS.TOKEN.CARB_BECH32_ADD,
                      "GZIL": CNSTS.TOKEN.GZIL_BECH32_ADD,
                      "SRV": CNSTS.TOKEN.SRV_BECH32_ADD,
                      "ZYRO": CNSTS.TOKEN.ZYRO_BECH32_ADD
                      }

account = Account(private_key=zutils.get_key(os.getenv(CONF.PRIM_WALLET['KEYSTORE']),
                                             os.getenv(CONF.PRIM_WALLET['PASSWORD'])
                                             ))

zilswap_contract = zutils.load_contract(CNSTS.CONTRACT.ZIL_SWAP_CONTRACT_ADD, account)
min_zils_per_token = 25
token_bech32 = tokens_of_interest['SRV']
token_per_to_sell = 0.1/100

initial_tokens = zutils.get_token_balance(token_bech32, zilswap_contract.account.bech32_address)
token_amount_to_sell = round(initial_tokens * token_per_to_sell)
tokens_remaining = initial_tokens


while tokens_remaining == initial_tokens:
    print("*"*100)
    print("min zils per token: ", min_zils_per_token)
    api_url = set_zil_api(api_url)
    code, msg = zilswap.limit_order(zilswap_contract,
                                    min_zils_per_token,
                                    token_bech32,
                                    token_amount_to_sell,
                                    gas_limit=CNSTS.ZLP_1HOP_SWAP_GAS_LIMIT,
                                    gas_price=CNSTS.ZLP_AVG_GAS_PRICE
                                    )
    if code == "Fail":
        print(msg)
    else:
        tokens_remaining = zutils.get_token_balance(token_bech32, zilswap_contract.account.bech32_address)
    print("Taking a break for a min.")
    min_zils_per_token = random.randint(20, 40)
    time.sleep(2)
