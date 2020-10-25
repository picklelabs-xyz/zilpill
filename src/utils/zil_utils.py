import getpass
import src.CONSTANTS as CNSTS
from src.pyzil_mod.account import Account as ModAccount
from pyzil.crypto import zilkey
from pyzil.contract import Contract
from pyzil.zilliqa.api import ZilliqaAPI, APIError


api = ZilliqaAPI(CNSTS.ZIL_API_URL)


def address0x(add):
    return "0x" + add


def to_base16_add(bech32_add):
    return address0x(zilkey.from_bech32_address(bech32_add))


def load_contract(contract_add):
    contract = Contract.load_from_address(contract_add)
    return contract


def get_key(keystore):
    password = getpass.getpass(prompt='Password: ')
    mod_account = ModAccount.from_keystore(password, keystore)
    return mod_account.private_key


def get_current_block():
    return api.GetCurrentMiniEpoch()
