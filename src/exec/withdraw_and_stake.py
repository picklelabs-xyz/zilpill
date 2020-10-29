import src.utils.zil_utils as zutils
import src.CONF as CONF
import os
import src.CONSTANTS as CNSTS
from src.stk import zillion
from os.path import join, dirname
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


rewards = zillion.withdraw_all_stake_rewards(zillion_contract, zillion_proxy_contract,
                                             ssn_adds, os.getenv(CONF.PRIM_WALLET['BECH32']))
print("Rewards: ", rewards)
if rewards > 50:
    # Put your SSN here to stake the rewards
    zillion.stake_zil(zillion_proxy_contract, CNSTS.SSN.SSN4_EZIL_BECH32, rewards)

