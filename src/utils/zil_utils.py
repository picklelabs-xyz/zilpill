import getpass
import src.CONSTANTS as CNSTS
import math
from src.pyzil_mod.account import Account as ModAccount
from pyzil.crypto import zilkey
from pyzil.contract import Contract
from pyzil.zilliqa.api import ZilliqaAPI, APIError


api = ZilliqaAPI(CNSTS.ZIL_API_URL)


def address0x(add):
    return "0x" + add


def to_base16_add(bech32_add):
    return address0x(zilkey.from_bech32_address(bech32_add))


def load_contract(contract_add, account=None):
    contract = Contract.load_from_address(contract_add)
    if account is None:
        return contract
    contract.account = account
    return contract


def get_key(keystore, password=None):
    if keystore is None:
        return None
    if password is None:
        password = getpass.getpass(prompt='Password: ')
    mod_account = ModAccount.from_keystore(password, keystore)
    return mod_account.private_key


def get_token_dec_divisor(token_contract):
    for param in token_contract.init:
        if param['vname'] == 'decimals':
            return math.pow(10, int(param['value']))


def get_token_balance(token_bech32, address_base16):
    token_contract = load_contract(token_bech32)
    token_dec_divisor = get_token_dec_divisor(token_contract)
    if address_base16 in token_contract.state['balances']:
        return int(token_contract.state['balances'][address_base16]) / token_dec_divisor
    return 0


def get_token_balances(tokens_bech32, token_dec_divisor, address_base16):
    token_contract = load_contract(tokens_bech32)
    if address_base16 in token_contract.state['balances']:
        return int(token_contract.state['balances'][address_base16]) / token_dec_divisor
    return 0


def get_current_block():
    return api.GetCurrentMiniEpoch()


def print_contract_details(contract, text_file=None):
    status = contract.status
    state = contract.state
    print(status)
    print(state)
    if text_file is not None:
        text_file = open(text_file, "w")
        text_file.write(str(status) + "\n" + str(state))
        text_file.close()





