import src.utils.zil_utils as zutils
import src.CONF as CONF
import os
import src.CONSTANTS as CNSTS
from src.stk import zillion
from src.utils import email_info
from datetime import datetime
from pyzil.account import Account
from dotenv import load_dotenv

load_dotenv()
personal_env = os.getenv(CONF.PERSONAL_ENV_FILE)
load_dotenv(personal_env)

# Put your keystore file path here or in CONF file
account = Account(private_key=zutils.get_key(os.getenv(CONF.PRIM_WALLET['KEYSTORE']),
                                             os.getenv(CONF.PRIM_WALLET['PASSWORD'])
                                             ))

# Load zillion staking contract with your own wallet
zillion_proxy_contract = zutils.load_contract(CNSTS.CONTRACT.ZILLION_CONTRACT_PROXY_ADD,
                                              account)

zillion_contract = zutils.load_contract(CNSTS.CONTRACT.ZILLION_CONTRACT_ADD,
                                        account)

# Put your SSNs here to withdraw the rewards
ssn_adds = [CNSTS.SSN.SSN1_VIEW_BLOCK_BECH32,
            CNSTS.SSN.SSN2_ZILLACRACY_BECH32,
            CNSTS.SSN.SSN3_MOONLET_BECH32,
            CNSTS.SSN.SSN4_EZIL_BECH32]

now = datetime.now()
dt = now.strftime("%d/%m/%Y %H:%M:%S")

rewards, info = zillion.withdraw_all_stake_rewards(zillion_contract, zillion_proxy_contract,
                                                   ssn_adds, os.getenv(CONF.PRIM_WALLET['BECH32']))
print("Rewards: ", rewards)
e_subject = "withdraw_and_stake: execution at " + dt

e_from_name = "Machine"
e_from_mail = os.getenv(CONF.EMAIL_1)
e_from_pwd = os.getenv(CONF.EMAIL_1_PASSWORD)
e_to_mails = [os.getenv(CONF.EMAIL_1)]

e_msg = 'Rewards withdrawn: ' + str(rewards) + '\n\n'
if rewards > 25:
    # Put your SSN here to stake the rewards
    success = zillion.stake_zil(zillion_proxy_contract, CNSTS.SSN.SSN4_EZIL_BECH32, rewards)
    e_msg = e_msg + 'Staking: ' + str(success) + '\n\n'


e_msg = e_msg + "\n".join(info)
e_msg = e_msg + "\n"
e_msg = e_msg + '\n' + 'Zillion: https://stake.zilliqa.com/address/' + os.getenv(CONF.PRIM_WALLET['BECH32'])
e_msg = e_msg + '\n' + 'Viewblock: https://viewblock.io/zilliqa/address/' + os.getenv(CONF.PRIM_WALLET['BECH32'])
email_info.mail_it(e_subject, e_msg, e_from_name, e_from_pwd, e_from_mail, e_to_mails)
