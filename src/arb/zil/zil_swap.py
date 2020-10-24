import src.CONSTANTS as CNSTS
import src.CONF as CONF
import src.utils.zil_utils as zutils
from pprint import pprint
from pyzil.zilliqa import chain
from pyzil.account import Account
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

def zilswap_zil_for_token_tx(contract, token_address, min_token_amount, deadline_block, recipient_address, z_amount):
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


zil_swap_contract = zutils.load_contract(CNSTS.ZIL_SWAP_CONTRACT_ADD)
# print(zil_swap_contract.status)
# pprint(zil_swap_contract.state)

zil_swap_gzil_price = get_token_price(get_contract_pools(CNSTS.ZIL_SWAP_CONTRACT_ADD),
                                      zutils.to_base16_add(CNSTS.GZIL_BECH32_ADD),
                                      CNSTS.GZIL_DEC_DIVISOR)
print(zil_swap_gzil_price)
print("gzil price in $")
print(zil_swap_gzil_price * 0.01971983)
print("gzil price in SGD")
print(zil_swap_gzil_price * 0.01971983 * 1.36)

# 1SGD = 0.74$

zil_swap_xsgd_price = get_token_price(get_contract_pools(CNSTS.ZIL_SWAP_CONTRACT_ADD),
                                      zutils.
                                      to_base16_add(CNSTS.XSGD_BECH32_PROXY_ADD),
                                      CNSTS.XSGD_DEC_DIVISOR)
print("sgd to zils")
print(zil_swap_xsgd_price)

account = Account(private_key=zutils.get_key(CONF.ZIL_WALLET_SEC_KEYSTORE))
balance = account.get_balance()
print("balance", balance)

zil_swap_contract.account = account

to_token_address = zutils.to_base16_add(CNSTS.XSGD_BECH32_PROXY_ADD)
min_token_amount_constraint = str(27282)  # The min amount here considers the token's decimal divisor
until_deadline_block = str(int(zutils.get_current_block()) + 10)
token_recipient_address = zutils.to_base16_add(CONF.ZIL_WALLET_THI_PUBLIC_ADD_BECH32)
z_amount = 5 * CNSTS.TEST_ZIL_AMOUNT

# Executes a test zil swap for converting zils to XSGD
## zilswap_zil_for_token_tx(zil_swap_contract, to_token_address, min_token_amount_constraint,
##                         until_deadline_block, token_recipient_address, z_amount)
