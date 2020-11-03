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
        # print(ssn_add_bech32, reward, info)
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


def get_wallet_deposits(zillion_contract, wallet_bech32):
    buff_deposit_delegate = zillion_contract.state['buff_deposit_deleg']
    deleg_stake_per_cycle = zillion_contract.state['deleg_stake_per_cycle']
    # ssn_deleg_amt = zillion_contract.state['ssn_deleg_amt']
    # withdrawal_pending = zillion_contract.state['withdrawal_pending']

    wallet_buff = buff_deposit_delegate[zutils.to_base16_add(wallet_bech32)]
    wallet_deleg_stake = deleg_stake_per_cycle[zutils.to_base16_add(wallet_bech32)]
    last_reward_cycle = zillion_contract.state['lastrewardcycle']

    wallet_buff_amnt = Zil(0)
    for ssn in wallet_buff:
        if last_reward_cycle in wallet_buff[ssn]:
            wallet_buff_amnt = wallet_buff_amnt + Qa(wallet_buff[ssn][last_reward_cycle]).toZil()
        second_last_reward_cycle = str(int(last_reward_cycle) - 1)
        if second_last_reward_cycle in wallet_buff[ssn]:
            wallet_buff_amnt = wallet_buff_amnt + Qa(wallet_buff[ssn][second_last_reward_cycle]).toZil()

    wallet_deleg_stake_amnt = Zil(0)
    for ssn in wallet_deleg_stake:
        if last_reward_cycle in wallet_deleg_stake[ssn]:
            wallet_deleg_stake_amnt = wallet_deleg_stake_amnt + Qa(wallet_deleg_stake[ssn][last_reward_cycle]).toZil()

    wallet_total_deposits = wallet_buff_amnt + wallet_deleg_stake_amnt
    return wallet_total_deposits


def check_if_rewards_claimed(zillion_contract_state, ssn_add_bech32, deleg_wallet_bech32):
    state = zillion_contract_state
    last_deleg_ssn_withdraw_cycle = state['last_withdraw_cycle_deleg'][zutils.to_base16_add(deleg_wallet_bech32)]
    last_deleg_ssn_withdraw_cycle = last_deleg_ssn_withdraw_cycle[zutils.to_base16_add(ssn_add_bech32)]
    last_reward_cycle = state['lastrewardcycle']
    if last_deleg_ssn_withdraw_cycle != last_reward_cycle:
        return False
    return True


def check_if_all_rewards_claimed(zillion_contract, ssn_adds_bech32, deleg_wallet_bech32):
    all_claimed = True
    zillion_contract_state = zillion_contract.state
    last_reward_cycle = zillion_contract_state['lastrewardcycle']
    for ssn_add_bech32 in ssn_adds_bech32:
        ssn_claimed = check_if_rewards_claimed(zillion_contract_state, ssn_add_bech32, deleg_wallet_bech32)
        all_claimed = ssn_claimed and all_claimed
        if not all_claimed:
            return all_claimed
    return all_claimed, last_reward_cycle
