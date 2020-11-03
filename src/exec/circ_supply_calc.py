import src.utils.zil_utils as zutils
import src.CONSTANTS as CNSTS
import os
import src.CONF as CONF
import json
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

# Put your SSNs here to withdraw the rewards
ssn_adds = [CNSTS.SSN.SSN1_VIEW_BLOCK_BECH32,
            CNSTS.SSN.SSN2_ZILLACRACY_BECH32,
            CNSTS.SSN.SSN3_MOONLET_BECH32,
            CNSTS.SSN.SSN4_EZIL_BECH32]

rewards_claimed, last_reward_cycle = zillion.check_if_all_rewards_claimed(zillion_contract, ssn_adds,
                                                                          os.getenv(CONF.PRIM_WALLET['BECH32']))

last_exec_json_file_path = "../../output/circ_supply_calc_last_exec.json"
last_exec_json = {}

if os.path.exists(last_exec_json_file_path):
    with open(last_exec_json_file_path) as last_exec_json_file:
        last_exec_json = json.load(last_exec_json_file)

json_last_reward_cycle = 0
if 'last_reward_cycle' in last_exec_json:
    json_last_reward_cycle = int(last_exec_json['last_reward_cycle'])

if rewards_claimed and int(last_reward_cycle) > json_last_reward_cycle:
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

    last_exec_json = {"execution_at": dt, "last_reward_cycle": int(last_reward_cycle)}
    with open(last_exec_json_file_path, 'w') as outfile:
        json.dump(last_exec_json, outfile)

