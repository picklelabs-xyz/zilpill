import src.CONSTANTS as CNSTS
import src.CONF as CONF
import src.utils.zil_utils as zutils
from pprint import pprint
from pyzil.zilliqa import chain
from pyzil.account import Account
from pyzil.contract import Contract

chain.set_active_chain(chain.MainNet)


def extract_reward_amount(resp):
    if 'receipt' in resp:
        receipt = resp['receipt']
        if 'event_logs' in receipt:
            event_logs = receipt['event_logs']
            for event_log in event_logs:
                if '_eventname' in event_log:
                    if 'WithdrawalStakeRewards' == event_log['_eventname']:
                        if 'params' in event_log:
                            for param in event_log['params']:
                                if param['vname'] == 'rewards':
                                    value = param['value']
                                    zil_rewards = int(value) / CNSTS.ZIL_DEC_DIVISOR
                                    return zil_rewards
    return 0


def withdraw_stake_rewards(contract, ssn_add_bech32):
    resp = contract.call(method="WithdrawStakeRewards",
                         params=[Contract.value_dict(
                             "ssnaddr",
                             "ByStr20",
                             zutils.to_base16_add(ssn_add_bech32))]
                         )
    pprint(resp)
    # pprint(contract.last_receipt)
    return extract_reward_amount(resp)


def withdraw_all_stake_rewards(contract, ssn_adds_bech32):
    total_reward = 0
    for ssn_add_bech32 in ssn_adds_bech32:
        reward = withdraw_stake_rewards(contract, ssn_add_bech32)
        total_reward = total_reward + reward
    return total_reward


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

zil_stake_contract = zutils.load_contract(CNSTS.SEED_NODE_STAKE_PROXY_BECH32)
zil_stake_contract.account = account

# Put your SSNs here to withdraw the rewards
ssn_adds = [CNSTS.SSN1_VIEW_BLOCK_BECH32, CNSTS.SSN2_ZILLACRACY_BECH32, CNSTS.SSN3_MOONLET_BECH32]

rewards = withdraw_all_stake_rewards(zil_stake_contract, ssn_adds)
print("Rewards: ", rewards)
if rewards > 10:
    stake_zil(zil_stake_contract, CNSTS.SSN4_EZIL_BECH32, rewards)

