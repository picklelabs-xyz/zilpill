import src.CONSTANTS as CNSTS
import src.CONF as CONF
import src.utils.zil_utils as zutils
from pprint import pprint
from pyzil.zilliqa import chain
from pyzil.account import Account
from pyzil.contract import Contract

chain.set_active_chain(chain.MainNet)


def withdraw_claim_rewards(contract, ssn_add_bech32):
    resp = contract.call(method="WithdrawStakeRewards",
                         params=[Contract.value_dict(
                             "ssnaddr",
                             "ByStr20",
                             zutils.to_base16_add(ssn_add_bech32))]
                         )
    pprint(resp)
    pprint(contract.last_receipt)


def withdraw_all_claim_rewards(contract, ssn_adds_bech32):
    for ssn_add_bech32 in ssn_adds_bech32:
        withdraw_claim_rewards(contract, ssn_add_bech32)


def stake_zil(contract, ssn_add_bech32, z_amount):
    resp = contract.call(method="DelegateStake",
                         params=[Contract.value_dict(
                             "ssnaddr",
                             "ByStr20",
                             zutils.to_base16_add(ssn_add_bech32))],
                         amount=z_amount)
    pprint(resp)
    pprint(contract.last_receipt)


# Put your keystore path here or in CONF file
account = Account(private_key=zutils.get_key(CONF.ZIL_WALLET_PRIM_KEYSTORE))
balance = account.get_balance()
print("balance", balance)

zil_stake_contract = zutils.load_contract(CNSTS.SEED_NODE_STAKE_PROXY_BECH32)
print(zil_stake_contract.status)
pprint(zil_stake_contract.state)

zil_stake_contract.account = account

# Put your SSNs here to withdraw the rewards
ssn_adds = [CNSTS.SSN1_VIEW_BLOCK_BECH32, CNSTS.SSN2_ZILLACRACY_BECH32, CNSTS.SSN3_MOONLET_BECH32]

# Uncomment the double commented withdraw function below before execution
## withdraw_all_claim_rewards(zil_stake_contract, ssn_adds)

# Currently, the amount is being put manually for re-staking here. Ideally,
# it should capture the amount of claimed rewards in the above withdraw function
# and then use that to stake, with the specified SSN
amount = 1000


# Uncomment the double commented stake function below before execution
# and specify the required SSN
## stake_zil(zil_stake_contract, CNSTS.SSN4_EZIL_BECH32, amount)

