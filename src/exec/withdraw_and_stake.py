import os
import src.utils.zil_utils as zutils
import src.CONSTANTS as CNSTS
from src.stk import zillion
from pyzil.account import Account
from dotenv import load_dotenv
load_dotenv()

# Put your keystore file path here or in CONF file
account = Account(private_key=zutils.get_key_env(os.getenv("ZIL_WALLET_PRIM_KEYSTORE"),
                                                 os.getenv("ZIL_WALLET_PRIM_PASSWORD")))

# Load zillion staking contract with your own wallet
zillion_contract = zillion.load_my_zillion(account)

# Put your SSNs here to withdraw the rewards
ssn_adds = [CNSTS.SSN1_VIEW_BLOCK_BECH32, CNSTS.SSN2_ZILLACRACY_BECH32,
            CNSTS.SSN3_MOONLET_BECH32, CNSTS.SSN4_EZIL_BECH32]

rewards = zillion.withdraw_all_stake_rewards(zillion_contract, ssn_adds)
print("Rewards: ", rewards)
if rewards > 10:
    # Put your SSN here to stake the rewards
    zillion.stake_zil(zillion_contract, CNSTS.SSN4_EZIL_BECH32, rewards)
