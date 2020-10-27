from pprint import pprint
from pyzil.zilliqa import chain
from pyzil.contract import Contract
from pyzil.zilliqa.units import Zil, Qa

chain.set_active_chain(chain.MainNet)

fees = 0.3


def get_contract_pools(contract):
    return contract.state['pools']


def get_token_pool_size(contract_pools, token_base_16, token_dec_divisor):
    token_pool = contract_pools[token_base_16]
    token_pool_args = token_pool['arguments']
    pool_zil_count = int(Qa(token_pool_args[0]).toZil())
    pool_token_count = int(token_pool_args[1])/token_dec_divisor
    return pool_token_count, pool_zil_count


def get_pool_token_sell_price(token_amount_to_be_sold, pool_token_count, pool_zil_count, fees):
    product = pool_token_count * pool_zil_count
    pool_token_amount_after_tx = pool_token_count + token_amount_to_be_sold
    token_price_for_tx = (pool_zil_count - product / pool_token_amount_after_tx) / token_amount_to_be_sold
    token_price_for_tx = token_price_for_tx - ((fees / 100) * token_price_for_tx)
    return token_price_for_tx


def sell_token_for_zil_tx(contract, token_address, token_amount, min_zil_amount, deadline_block, recipient_address):
    resp = contract.call(method="SwapExactTokensForZIL",
                         params=[Contract.value_dict("token_address", "ByStr20", token_address),
                                 Contract.value_dict("token_amount", "Uint128", token_amount),
                                 Contract.value_dict("min_zil_amount", "Uint128", min_zil_amount),
                                 Contract.value_dict("deadline_block", "BNum", deadline_block),
                                 Contract.value_dict("recipient_address", "ByStr20", recipient_address)
                                 ],
                         gas_limit=30000
                         )

    pprint(resp)
    pprint(contract.last_receipt)


def sell_zil_for_token_tx(contract, token_address, min_token_amount, deadline_block, recipient_address, z_amount):
    resp = contract.call(method="SwapExactZILForTokens",
                         params=[Contract.value_dict("token_address", "ByStr20", token_address),
                                 Contract.value_dict("min_token_amount", "Uint128", min_token_amount),
                                 Contract.value_dict("deadline_block", "BNum", deadline_block),
                                 Contract.value_dict("recipient_address", "ByStr20", recipient_address)
                                 ],
                         gas_limit=30000,
                         amount=z_amount)

    pprint(resp)
    pprint(contract.last_receipt)


# Needs to be tested
def zilswap_token_for_token_tx(contract, token0_address, token1_address, token0_amount,
                               min_token1_amount, deadline_block, recipient_address):
    resp = contract.call(method="SwapExactTokensForTokens",
                         params=[Contract.value_dict("token0_address", "ByStr20", token0_address),
                                 Contract.value_dict("token1_address", "ByStr20", token1_address),
                                 Contract.value_dict("token0_amount", "Uint128", token0_amount),
                                 Contract.value_dict("min_token_amount", "Uint128", min_token1_amount),
                                 Contract.value_dict("deadline_block", "BNum", deadline_block),
                                 Contract.value_dict("recipient_address", "ByStr20", recipient_address)
                                 ])
    pprint(resp)
    pprint(contract.last_receipt)






