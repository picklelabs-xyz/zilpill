import src.utils.zil_utils as zutils
import src.CONF as CONF
import os
import src.CONSTANTS as CNSTS
from src.arb.zil import zilswap
from src.stk import zillion
from pyzil.account import Account
from dotenv import load_dotenv
from pyzil.zilliqa import chain

vMainNet = chain.BlockChain(zutils.get_zil_api_url(), version=65537, network_id=1)
chain.set_active_chain(vMainNet)

load_dotenv()
personal_env = os.getenv(CONF.PERSONAL_ENV_FILE)
load_dotenv(personal_env)

tokens_of_interest = {"ZCH": CNSTS.TOKEN.ZCH_BECH32_ADD,
                      "XSGD": CNSTS.TOKEN.XSGD_BECH32_ADD,
                      "ZWAP": CNSTS.TOKEN.ZWAP_BECH32_ADD,
                      "CARB": CNSTS.TOKEN.CARB_BECH32_ADD,
                      "GZIL": CNSTS.TOKEN.GZIL_BECH32_ADD,
                      "SRV": CNSTS.TOKEN.SRV_BECH32_ADD,
                      "ZYRO": CNSTS.TOKEN.ZYRO_BECH32_ADD
                      }

# account = Account(private_key=zutils.get_key(os.getenv(CONF.PRIM_WALLET['KEYSTORE']),
#                                              os.getenv(CONF.PRIM_WALLET['PASSWORD'])
#                                              ))
# user_wallet_bech32 = account.bech32_address

user_wallet_bech32 = os.getenv(CONF.PRIM_WALLET['BECH32'])
account = Account(address=user_wallet_bech32)
balance = account.get_balance()
user_zil_bal = account.get_balance()
print("User address: ", user_wallet_bech32)

zillion_contract = zutils.load_contract(CNSTS.CONTRACT.ZILLION_CONTRACT_ADD, account)
user_staked_zil = zillion.get_wallet_deposits(zillion_contract, user_wallet_bech32)

zilswap_contract = zutils.load_contract(CNSTS.CONTRACT.ZIL_SWAP_CONTRACT_ADD, account)
user_total_pooled_amount_in_zil = zilswap.get_pooled_assets_in_zil(zilswap_contract,
                                                                   tokens_of_interest,
                                                                   user_wallet_bech32)

zil_usd_price = None
zil_sgd_price = zilswap.get_zil_xsgd_price(zilswap_contract, user_total_pooled_amount_in_zil)
zil_usd_price = zil_sgd_price * CNSTS.SGD
print(zil_usd_price)

user_total_zil = round(float(user_zil_bal) + user_total_pooled_amount_in_zil + user_staked_zil, 2)
print("User total pooled and staked amount in zil: ", user_total_zil, " - ",
      round(user_total_zil * zil_usd_price, 2), "$")