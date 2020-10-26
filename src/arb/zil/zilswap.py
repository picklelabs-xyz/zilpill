import src.CONSTANTS as CNSTS
import src.utils.zil_utils as zutils
from pprint import pprint
from pyzil.zilliqa import chain
from pyzil.contract import Contract

chain.set_active_chain(chain.MainNet)


def get_contract_pools(contract_add):
    contract = zutils.load_contract(contract_add)
    return contract.state['pools']


def get_token_price(contract_pools, token_base_16, decimal_divisor):
    token_pool = contract_pools[token_base_16]
    token_pool_args = token_pool['arguments']
    pool_zil_count = int(token_pool_args[0])/CNSTS.ZIL_DEC_DIVISOR
    pool_token_count = int(token_pool_args[1])/decimal_divisor
    token_price_in_zil = pool_zil_count/pool_token_count
    return token_price_in_zil


#   sample
#   token_address
#   0x173ca6770aa56eb00511dac8e6e13b3d7f16a5a5
#   min_token_amount
#   "27282"
#   deadline_block
#   "842717"
#   recipient_address
#   0xf294ad809628faad9235e5c42908146bea4c30d5


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


#  Sample
#  token0_address	0xa845c1034cd077bd8d32be0447239c7e4be6cb21
#  token1_address	0x173ca6770aa56eb00511dac8e6e13b3d7f16a5a5
#  token0_amount
#  "1000000000000"
#  min_token1_amount
#  "74551"
#  deadline_block
#  "842729"
#  recipient_address	0xf294ad809628faad9235e5c42908146bea4c30d5
# def zilswap_token_for_token_tx(contract, token0_address, token1_address, token0_amount,
#                                min_token1_amount, deadline_block, recipient_address):
#     resp = contract.call(method="SwapExactTokensForTokens",
#                          params=[Contract.value_dict("token0_address", "ByStr20", token0_address),
#                                  Contract.value_dict("token1_address", "ByStr20", token1_address),
#                                  Contract.value_dict("token0_amount", "Uint128", token0_amount),
#                                  Contract.value_dict("min_token_amount", "Uint128", min_token1_amount),
#                                  Contract.value_dict("deadline_block", "BNum", deadline_block),
#                                  Contract.value_dict("recipient_address", "ByStr20", recipient_address)
#                                  ])
#     pprint(resp)
#     pprint(contract.last_receipt)

def load_my_zilswap(account=None):
    contract = zutils.load_contract(CNSTS.ZIL_SWAP_CONTRACT_ADD)
    if account is None:
        return contract
    contract.account = account
    return contract




