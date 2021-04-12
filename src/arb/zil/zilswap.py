import src.utils.zil_utils as zutils
import src.CONSTANTS as CNSTS
from pprint import pprint
from pyzil.zilliqa import chain
from pyzil.contract import Contract
from pyzil.zilliqa.units import Zil, Qa


chain.set_active_chain(chain.MainNet)

fees = 0.3


def get_contract_pools(contract):
    return contract.state['pools']


def get_balances(contract):
    return contract.state['balances']


def get_total_contributions(contract):
    return contract.state['total_contributions']


def get_user_token_pool_contri(contract, token_bech32, user_bech32):
    pools = get_contract_pools(contract)
    balances = get_balances(contract)
    total_contributions = get_total_contributions(contract)
    token_base16 = zutils.to_base16_add(token_bech32)
    token_dec_divisor = zutils.get_token_dec_divisor(zutils.load_contract(token_bech32))
    token_balances = balances[token_base16]
    token_total_contributions = int(total_contributions[token_base16])
    user_base16 = zutils.to_base16_add(user_bech32)
    user_token_pool_contribution = 0.0
    if user_base16 in token_balances:
        user_token_pool_contribution = int(token_balances[zutils.to_base16_add(user_bech32)])
    token_zil_pool_bal = pools[token_base16]
    zil_pool_bal = int(Qa(token_zil_pool_bal['arguments'][0]).toZil())
    token_pool_bal = int(token_zil_pool_bal['arguments'][1]) / token_dec_divisor
    user_share_per = user_token_pool_contribution / token_total_contributions
    return round(user_share_per * 100, 4), user_share_per * zil_pool_bal, user_share_per * token_pool_bal


def get_pooled_assets_in_zil(contract, tokens, user_wallet_bech32):
    total_zil_pooled = 0
    for token in tokens:
        print("*" * 100)
        token_bech32 = tokens[token]
        user_wallet_token_bal = zutils.get_token_balance(token_bech32, user_wallet_bech32)
        amount_to_gauge_price = user_wallet_token_bal
        if user_wallet_token_bal <= 2:
            amount_to_gauge_price = 1
        token_zil_price = get_token_zil_price(contract, token_bech32, amount_to_gauge_price)
        user_token_zil_bal = token_zil_price * user_wallet_token_bal
        print(token,
              " user bal: ", user_wallet_token_bal,
              " price in zils: ", token_zil_price,
              " value in zils: ", user_token_zil_bal)
        user_share_per, user_token_pool_zil_bal, user_token_pool_token_bal = \
            get_user_token_pool_contri(contract, token_bech32, user_wallet_bech32)
        print(token, " pool : ",
              user_share_per, " : Zil - ",
              user_token_pool_zil_bal, " :",
              token, " - ", user_token_pool_token_bal)

        total_zil_pooled += user_token_pool_zil_bal * 2
        total_zil_pooled += user_token_zil_bal
        print("*" * 100)

    return total_zil_pooled


def get_token_pool_size(contract, token_bech32):
    token_base16 = zutils.to_base16_add(token_bech32)
    token_dec_divisor = zutils.get_token_dec_divisor(zutils.load_contract(token_bech32))
    pools = get_contract_pools(contract)
    token_pool = pools[token_base16]
    token_pool_args = token_pool['arguments']
    pool_zil_count = int(Qa(token_pool_args[0]).toZil())
    pool_token_count = int(token_pool_args[1])/token_dec_divisor
    return pool_token_count, pool_zil_count


def get_token_zil_price(contract, token_bech32, token_amount):
    pool_token_count, pool_zil_count = get_token_pool_size(contract, token_bech32)
    token_price_for_tx = get_pool_token_sell_price(token_amount,
                                                   pool_token_count,
                                                   pool_zil_count)
    token_price_for_tx = round(token_price_for_tx, 2)
    return token_price_for_tx


def get_zil_xsgd_price(contract, zil_amount):
    token_bech32 = CNSTS.TOKEN.XSGD_BECH32_ADD
    pool_token_count, pool_zil_count = get_token_pool_size(contract, token_bech32)
    return get_pool_token_sell_price(zil_amount, pool_zil_count, pool_token_count)


def get_pool_token_sell_price(token_amount_to_be_sold, pool_token_count, pool_zil_count):
    product = pool_token_count * pool_zil_count
    pool_token_amount_after_tx = pool_token_count + token_amount_to_be_sold
    token_price_for_tx = (pool_zil_count - product / pool_token_amount_after_tx) / token_amount_to_be_sold
    token_price_for_tx = token_price_for_tx - ((fees / 100) * token_price_for_tx)
    return token_price_for_tx


def sell_token_for_zil_tx(contract, token_address, token_amount, min_zil_amount, deadline_block, recipient_address,
                          gas_limit, gas_price):
    resp = contract.call(method="SwapExactTokensForZIL",
                         params=[Contract.value_dict("token_address", "ByStr20", token_address),
                                 Contract.value_dict("token_amount", "Uint128", token_amount),
                                 Contract.value_dict("min_zil_amount", "Uint128", min_zil_amount),
                                 Contract.value_dict("deadline_block", "BNum", deadline_block),
                                 Contract.value_dict("recipient_address", "ByStr20", recipient_address)
                                 ],
                         gas_limit=gas_limit,
                         gas_price=gas_price
                         )
    pprint(resp)
    pprint(contract.last_receipt)


def sell_zil_for_token_tx(contract, token_address, min_token_amount, deadline_block, recipient_address, z_amount,
                          gas_limit, gas_price):
    resp = contract.call(method="SwapExactZILForTokens",
                         params=[Contract.value_dict("token_address", "ByStr20", token_address),
                                 Contract.value_dict("min_token_amount", "Uint128", min_token_amount),
                                 Contract.value_dict("deadline_block", "BNum", deadline_block),
                                 Contract.value_dict("recipient_address", "ByStr20", recipient_address)
                                 ],
                         gas_limit=gas_limit,
                         gas_price=gas_price,
                         amount=z_amount)
    pprint(resp)
    pprint(contract.last_receipt)


# Needs to be tested
def zilswap_token_for_token_tx(contract, token0_address, token1_address, token0_amount,
                               min_token1_amount, deadline_block, recipient_address,
                               gas_limit, gas_price):
    resp = contract.call(method="SwapExactTokensForTokens",
                         params=[Contract.value_dict("token0_address", "ByStr20", token0_address),
                                 Contract.value_dict("token1_address", "ByStr20", token1_address),
                                 Contract.value_dict("token0_amount", "Uint128", token0_amount),
                                 Contract.value_dict("min_token_amount", "Uint128", min_token1_amount),
                                 Contract.value_dict("deadline_block", "BNum", deadline_block),
                                 Contract.value_dict("recipient_address", "ByStr20", recipient_address)
                                 ],
                         gas_limit=gas_limit,
                         gas_price=gas_price
                         )
    pprint(resp)
    pprint(contract.last_receipt)


# Needs to be tested
def add_liquidity(contract, token_address, min_contribution_amount, max_token_amount, deadline_block,
                  gas_limit, gas_price):
    resp = contract.call(method="AddLiquidity",
                         params=[Contract.value_dict("token_address", "ByStr20", token_address),
                                 Contract.value_dict("min_contribution_amount", "ByStr20", min_contribution_amount),
                                 Contract.value_dict("max_token_amount", "Uint128", max_token_amount),
                                 Contract.value_dict("deadline_block", "BNum", deadline_block)
                                 ],
                         gas_limit=gas_limit,
                         gas_price=gas_price
                         )
    pprint(resp)
    pprint(contract.last_receipt)


# Needs to be tested
def remove_liquidity(contract, token_address, contribution_amount, min_zil_amount, min_token_amount, deadline_block,
                     gas_limit, gas_price):
    resp = contract.call(method="RemoveLiquidity",
                         params=[Contract.value_dict("token_address", "ByStr20", token_address),
                                 Contract.value_dict("contribution_amount", "Uint128", contribution_amount),
                                 Contract.value_dict("min_zil_amount", "Uint128", min_zil_amount),
                                 Contract.value_dict("min_token_amount", "Uint128", min_token_amount),
                                 Contract.value_dict("deadline_block", "BNum", deadline_block)
                                 ],
                         gas_limit=gas_limit,
                         gas_price=gas_price
                         )
    pprint(resp)
    pprint(contract.last_receipt)



def limit_order(contract,
                min_zils_per_token,
                token_bech32,
                token_amount_to_sell = None,
                recipient_address_bech32 = None,
                allowed_slippage_per = 2/100,
                gas_limit=5000,
                gas_price=Qa(2000000000)
                ):
    if recipient_address_bech32 is None:
        recipient_address_bech32 = contract.account.bech32_address
    if token_amount_to_sell is None:
        return "Fail", "No tokens to sell"
    print("To sell :", token_amount_to_sell)

    price_per_token = get_token_zil_price(contract,
                                          token_bech32,
                                          token_amount_to_sell)
    print("Current price per unit: ", price_per_token)
    if price_per_token < min_zils_per_token:
        return "Fail", "Current price lower than target minimum price, before slippage"

    min_zil_amount = price_per_token * token_amount_to_sell
    min_zil_amount = min_zil_amount - (allowed_slippage_per * min_zil_amount)
    print("Min zil to get after slippage:", min_zil_amount)
    min_zil_amount = str(Zil(min_zil_amount).toQa())
    print("Min zil (with decimals) to get :", min_zil_amount)

    token_dec_divisor = zutils.get_token_dec_divisor(zutils.load_contract(token_bech32))
    token_amount_to_sell = token_amount_to_sell * token_dec_divisor
    token_amount_to_sell = str(round(token_amount_to_sell))
    print("Token (with decimals) to sell  :", token_amount_to_sell)

    deadline_block = str(zutils.get_current_block() + CNSTS.DEADLINE_IN_BLOCKS)
    recipient_address_base16 = zutils.to_base16_add(recipient_address_bech32)
    return "Success", sell_token_for_zil_tx(contract, zutils.to_base16_add(token_bech32),
                                            token_amount_to_sell, min_zil_amount,
                                            deadline_block, recipient_address_base16,
                                            gas_limit, gas_price)




