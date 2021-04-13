import math
from pyzil.zilliqa.units import Zil, Qa

# Got all the below addresses/info from https://viewblock.io/zilliqa

ZILLIQA_API_URL = "https://api.zilliqa.com/"
ZILLET_API_URL = "https://ssn.zillet.io"
KUCOIN_API_URL = "https://staking-zil.kucoin.com/api"
# VIEWBLOCK_API_URL = "https://ssn-api-mainnet.viewblock.io" It does not seem working
EZIL_API_URL = "https://zil-staking.ezil.me/api"
ZILLIQA_STAKING_API_URL = "https://stakingseed-api.seed.zilliqa.com"
ZILLACRACY_API_URL = "https://ssn.zillacracy.com/api"



ZIL_API_URL_BASKET = (ZILLIQA_API_URL, ZILLET_API_URL, KUCOIN_API_URL,
                      EZIL_API_URL, ZILLIQA_STAKING_API_URL, ZILLACRACY_API_URL)


# Supply URL obtained from coingecko's zil page
ZIL_SUPPLY_URL = "https://stat.zilliqa.com/api/supply"



# Contracts
class CONTRACT:
    ZIL_SWAP_CONTRACT_ADD = "zil1hgg7k77vpgpwj3av7q7vv5dl4uvunmqqjzpv2w"
    ZILLION_CONTRACT_PROXY_ADD = "zil1g029nmzsf36r99vupp4s43lhs40fsscx3jjpuy"
    ZILLION_CONTRACT_ADD = "zil1k7qwsz2m3w595u29je0dvv4nka62c5wwrp8r8p"
    ZIL_CHESS_CONTRACT_ADD = "zil18m9qjcf2l22mhl4mxxxutcdprsw5xuclvhwglq"


# Token Contracts
class TOKEN:
    GZIL_BECH32_ADD = 'zil14pzuzq6v6pmmmrfjhczywguu0e97djepxt8g3e'
    XSGD_BECH32_ADD = 'zil1zu72vac254htqpg3mtywdcfm84l3dfd9qzww8t'
    ZCH_BECH32_ADD = 'zil1s8xzysqcxva2x6aducncv9um3zxr36way3fx9g'
    SRV_BECH32_ADD = "zil168qdlq4xsua6ac9hugzntqyasf8gs7aund882v"
    ZWAP_BECH32_ADD = 'zil1p5suryq6q647usxczale29cu3336hhp376c627'
    CARB_BECH32_ADD = 'zil1hau7z6rjltvjc95pphwj57umdpvv0d6kh2t8zk'
    ZYRO_BECH32_ADD = 'zil1ucvrn22x8366vzpw5t7su6eyml2auczu6wnqqg'


# SSN (Seed Stake Node) Operator Addresses
class SSN:
    SSN1_VIEW_BLOCK_BECH32 = "zil1s2uzcefp8c9jkgryjtfa3g4x08nlu5hq3ryj4h"
    SSN2_ZILLACRACY_BECH32 = "zil1hqlu93evgjmts6wxgwzrwhyhnhpl0nc96l2xtm"
    SSN3_MOONLET_BECH32 = "zil1vd007cj6z378egpew3z7aepkz20wdjst789ucx"
    SSN4_EZIL_BECH32 = "zil19tlfux8d6wweylg0llufjpsjl3905g54u5akjx"
    SSN4_EZIL_BASE16 = "0x2afe9e18edd39d927d0ffff8990612fc4afa2295"


# Using block stats chart from viewblock, approx 52K transactions in a month
NUM_BLOCKS_IN_1_MIN = round(52000/(31*24*60))

# Assuming as a constant for now
SGD = 0.74  # $

TEST_ZIL_AMOUNT = 1

DEADLINE_IN_BLOCKS = 15


ZLP_AVG_GAS_PRICE = Qa(2000000000)
ZLP_FAST_GAS_PRICE = Qa(4000000000)
ZLP_FANTASTIC_GAS_PRICE = Qa(18000000000)
ZLP_1HOP_SWAP_GAS_LIMIT = 5000
ZLP_LP_REMOVE_GAS_LIMIT = 5000
