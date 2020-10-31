import src.utils.zil_utils as zutils
import src.CONF as CONF
import os
import src.CONSTANTS as CNSTS
from src.arb.zil import zilswap
from pyzil.account import Account
from dotenv import load_dotenv

load_dotenv()
personal_env = os.getenv(CONF.PERSONAL_ENV_FILE)
load_dotenv(personal_env)

# Put your keystore file path here or in CONF file
account = Account(private_key=zutils.get_key(os.getenv(CONF.SEC_WALLET['KEYSTORE']),
                                             os.getenv(CONF.SEC_WALLET['PASSWORD'])
                                             ))

# Load zillion staking contract with your own wallet
zilswap_contract = zutils.load_contract(CNSTS.CONTRACT.ZIL_SWAP_CONTRACT_ADD,
                                              account)

pools = zilswap.get_contract_pools(zilswap_contract)

pool_token_count, pool_zil_count = zilswap.get_token_pool_size(
    pools,
    zutils.to_base16_add(CNSTS.TOKEN.GZIL_BECH32_ADD),
    zutils.get_token_dec_divisor(zutils.load_contract(CNSTS.TOKEN.GZIL_BECH32_ADD)))

token_amount_to_be_sold = 10
fees = zilswap.fees

token_price_for_tx = zilswap.get_pool_token_sell_price(token_amount_to_be_sold,
                                  pool_token_count,
                                  pool_zil_count,
                                  fees)
print("Current GZIL price for ", token_amount_to_be_sold, " units: ", token_price_for_tx)