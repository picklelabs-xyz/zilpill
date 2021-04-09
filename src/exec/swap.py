import src.utils.zil_utils as zutils
import src.CONF as CONF
import os
import src.CONSTANTS as CNSTS
from datetime import datetime
from src.utils import email_info
from src.arb.zil import zilswap
from pyzil.account import Account
from dotenv import load_dotenv
from pyzil.zilliqa.units import Zil, Qa
from pyzil.zilliqa import chain

vMainNet = chain.BlockChain(zutils.get_zil_api_url(), version=65537, network_id=1)
chain.set_active_chain(vMainNet)

load_dotenv()
personal_env = os.getenv(CONF.PERSONAL_ENV_FILE)
load_dotenv(personal_env)

# Put your keystore file path here or in CONF file
account = Account(private_key=zutils.get_key(os.getenv(CONF.PRIM_WALLET['KEYSTORE']),
                                             os.getenv(CONF.PRIM_WALLET['PASSWORD'])
                                             ))

# Load zillion staking contract with your own wallet
zilswap_contract = zutils.load_contract(CNSTS.CONTRACT.ZIL_SWAP_CONTRACT_ADD,
                                        account)


tokens_of_interest = {"ZCH": CNSTS.TOKEN.ZCH_BECH32_ADD,
                      "XSGD": CNSTS.TOKEN.XSGD_BECH32_ADD,
                      "ZWAP": CNSTS.TOKEN.ZWAP_BECH32_ADD,
                      "CARB": CNSTS.TOKEN.CARB_BECH32_ADD,
                      'GZIL': CNSTS.TOKEN.GZIL_BECH32_ADD
                      }

user_total_pooled_amount_in_zil = 0

user_wallet_bech32 = os.getenv(CONF.PRIM_WALLET['BECH32'])
print("User address: ", user_wallet_bech32)
total_zil_pooled = 0
zil_usd_price = None

for token in tokens_of_interest:
    token_bech32 = tokens_of_interest[token]
    user_share_per, user_token_pool_zil_bal, user_token_pool_token_bal = \
        zilswap.get_user_token_pool_contri(zilswap_contract,
                                           token_bech32,
                                           user_wallet_bech32)
    print(token, " pool : ",
          user_share_per, " : Zil - ",
          user_token_pool_zil_bal, " :",
          token, " - ", user_token_pool_token_bal)

    total_zil_pooled += user_token_pool_zil_bal * 2

zil_sgd_price = zilswap.get_zil_xsgd_price(zilswap_contract, total_zil_pooled)
zil_usd_price = zil_sgd_price * CNSTS.SGD
print(zil_usd_price)
print("User total pooled amount in zil: ", total_zil_pooled, " - ", round(total_zil_pooled * zil_usd_price, 2), "$")

