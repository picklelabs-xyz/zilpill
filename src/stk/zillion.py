import src.utils.zil_utils as zutils
from pprint import pprint
from pyzil.zilliqa import chain
from pyzil.contract import Contract
from pyzil.zilliqa.units import Zil, Qa

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
                                    zil_rewards = Qa(value).toZil()
                                    return float(zil_rewards)
    return 0


def extract_receipt_response(resp):
    if 'receipt' in resp:
        receipt = resp['receipt']
        success = receipt['success']
        return success
    return False


def extract_receipt(resp, contract):
    # Sometimes, the last receipt/resp can be received as none, even if the tx went through
    # In those cases, getting the last tx id from account, and use it to retrieve further info
    if resp is None:
        if contract.last_receipt is not None:
            resp = {'receipt': contract.last_receipt}
        else:
            tx_info = zutils.api.GetTransaction(contract.account.last_txn_info['TranID'])
            resp = {'receipt': tx_info['receipt']}
    return resp


def withdraw_stake_rewards(zillion_contract, zillion_proxy_contract, ssn_add_bech32, deleg_wallet_bech32):
    details_from = 'resp'  # just to track debug info
    rewards = 0
    state = zillion_contract.state
    last_deleg_ssn_withdraw_cycle = state['last_withdraw_cycle_deleg'][zutils.to_base16_add(deleg_wallet_bech32)]
    last_deleg_ssn_withdraw_cycle = last_deleg_ssn_withdraw_cycle[zutils.to_base16_add(ssn_add_bech32)]

    last_reward_cycle = state['lastrewardcycle']
    if last_deleg_ssn_withdraw_cycle != last_reward_cycle:
        resp = zillion_proxy_contract.call(method="WithdrawStakeRewards",
                                           params=[Contract.value_dict(
                                               "ssnaddr",
                                               "ByStr20",
                                               zutils.to_base16_add(ssn_add_bech32))]
                                           )
        resp = extract_receipt(resp, zillion_proxy_contract)
        rewards = extract_reward_amount(resp)
    return rewards, details_from


def withdraw_all_stake_rewards(zillion_contract, zillion_proxy_contract, ssn_adds_bech32, deleg_wallet_bech32):
    all_info = []
    total_reward = 0
    for ssn_add_bech32 in ssn_adds_bech32:
        reward, info = withdraw_stake_rewards(zillion_contract, zillion_proxy_contract,
                                              ssn_add_bech32, deleg_wallet_bech32)
        print(ssn_add_bech32, reward, info)
        all_info.append(ssn_add_bech32 + " " + str(reward) +  " " + info)
        total_reward = total_reward + reward
    return total_reward, all_info


def stake_zil(zillion_proxy_contract, ssn_add_bech32, z_amount):
    resp = zillion_proxy_contract.call(method="DelegateStake",
                                       params=[Contract.value_dict(
                                           "ssnaddr",
                                           "ByStr20",
                                           zutils.to_base16_add(ssn_add_bech32))],
                                       amount=z_amount)
    resp = extract_receipt(resp, zillion_proxy_contract)
    success = extract_receipt_response(resp)
    print(success)
    return success
