import src.utils.zil_utils as zutils
import src.CONSTANTS as CNSTS
import os
import src.CONF as CONF
from src.stk import zillion
from src.utils import email_info
from datetime import datetime
from pyzil.account import Account
from dotenv import load_dotenv

load_dotenv()
personal_env = os.getenv(CONF.PERSONAL_ENV_FILE)
load_dotenv(personal_env)

# Put your keystore file path here or in CONF file
account = Account(os.getenv(CONF.PRIM_WALLET['BECH32']))

now = datetime.now()
dt = now.strftime("%d/%m/%Y %H:%M:%S")

zillion_contract = zutils.load_contract(CNSTS.CONTRACT.ZILLION_CONTRACT_ADD, account)

wallet_total_deposits = zillion.get_wallet_deposits(zillion_contract, os.getenv(CONF.PRIM_WALLET['BECH32']))
circulating_supply = zutils.get_circulating_supply()
wallet_deposit_as_per_circ_supply = (float(wallet_total_deposits) / circulating_supply) * 100

e_subject = "circ_supply_calc: execution at " + dt
e_from_name = "Machine"
e_from_mail = os.getenv(CONF.EMAIL_1)
e_from_pwd = os.getenv(CONF.EMAIL_1_PASSWORD)
e_to_mails = [os.getenv(CONF.EMAIL_1)]

e_msg = []
e_msg.append("Wallet staked amount is "
             + str(round(wallet_deposit_as_per_circ_supply, 7))
             + ' % of circulating supply i.e. '
             + str(round(wallet_total_deposits, 2)) + " / " + str(round(float(circulating_supply), 2)))

e_msg.append('\n')
e_msg.append('Zillion: https://stake.zilliqa.com/address/' + os.getenv(CONF.PRIM_WALLET['BECH32']))
e_msg.append('Viewblock: https://viewblock.io/zilliqa/address/' + os.getenv(CONF.PRIM_WALLET['BECH32']))
e_msg.append('Zil circ supply: ' + CNSTS.ZIL_SUPPLY_URL)
print("\n".join(e_msg))

email_info.mail_it(e_subject, "\n".join(e_msg), e_from_name, e_from_pwd, e_from_mail, e_to_mails)
