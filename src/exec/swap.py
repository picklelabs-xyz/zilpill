import src.utils.zil_utils as zutils
import src.CONF as CONF
import os
import src.CONSTANTS as CNSTS
from datetime import datetime
from src.utils import email_info
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

now = datetime.now()
dt = now.strftime("%d/%m/%Y %H:%M:%S")

pool_token_count, pool_zil_count = zilswap.get_token_pool_size(
    pools,
    zutils.to_base16_add(CNSTS.TOKEN.GZIL_BECH32_ADD),
    zutils.get_token_dec_divisor(zutils.load_contract(CNSTS.TOKEN.GZIL_BECH32_ADD)))

fees = zilswap.fees

token_amounts = [1, 10, 20]
token_amount_and_price = {}
infos = []

for token_amount in token_amounts:
    token_price_for_tx = zilswap.get_pool_token_sell_price(token_amount,
                                                           pool_token_count,
                                                           pool_zil_count,
                                                           fees)
    token_price_for_tx = round(token_price_for_tx)
    info = "GZIL token price, if selling " + str(token_amount) + " units: " + str(token_price_for_tx)
    token_amount_and_price[token_amount] = token_price_for_tx
    infos.append(info)

e_subject = "swap: execution at " + dt
e_from_name = "Machine"
e_from_mail = os.getenv(CONF.EMAIL_1)
e_from_pwd = os.getenv(CONF.EMAIL_1_PASSWORD)
e_to_mails = [os.getenv(CONF.EMAIL_1), os.getenv(CONF.EMAIL_2)]
e_msg = "\n".join(infos)

print("\n")
print(e_subject)
print(e_msg)

if token_amount_and_price[token_amounts[1]] > 2500:
    email_info.mail_it(e_subject, e_msg, e_from_name, e_from_pwd, e_from_mail, e_to_mails)
