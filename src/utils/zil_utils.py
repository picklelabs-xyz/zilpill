import getpass
import src.CONSTANTS as CNSTS
import math
import requests
import src.CONF as CONF
import os
import random
from src.pyzil_mod.account import Account as ModAccount
from pyzil.crypto import zilkey
from pyzil.contract import Contract
from pyzil.zilliqa import chain
from dotenv import load_dotenv
from pyzil.zilliqa.api import ZilliqaAPI, APIError


def get_zil_api_url():
    return random.choice(CNSTS.ZIL_API_URL_BASKET)


api = ZilliqaAPI(get_zil_api_url())
link = CNSTS.ZIL_SUPPLY_URL


def set_zil_api(last_api_url=CNSTS.ZILLIQA_API_URL):
    api_url = get_zil_api_url()
    while last_api_url==api_url:
        api_url = get_zil_api_url()
    print(api_url)
    vMainNet = chain.BlockChain(api_url, version=65537, network_id=1)
    chain.set_active_chain(vMainNet)
    return api_url


def set_env():
    load_dotenv()
    personal_env = os.getenv(CONF.PERSONAL_ENV_FILE)
    load_dotenv(personal_env)


def address0x(add):
    return "0x" + add


def to_base16_add(bech32_add):
    return address0x(zilkey.from_bech32_address(bech32_add))


def to_bech32_address(base16_add):
    return zilkey.to_bech32_address(base16_add)


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


def get_token_balance(token_bech32, address_bech32, token_dec_divisor=None):
    address_base16 = to_base16_add(address_bech32)
    token_contract = load_contract(token_bech32)
    if token_dec_divisor is None:
        token_dec_divisor = get_token_dec_divisor(token_contract)
    if address_base16 in token_contract.state['balances']:
        return int(token_contract.state['balances'][address_base16]) / token_dec_divisor
    return 0


def get_current_block():
    return int(api.GetCurrentMiniEpoch())


def print_contract_details(contract, text_file=None):
    status = contract.status
    state = contract.state
    print(status)
    print(state)
    if text_file is not None:
        text_file = open(text_file, "w")
        text_file.write(str(status) + "\n" + str(state))
        text_file.close()


def get_circulating_supply():
    return float(requests.get(link).text)




