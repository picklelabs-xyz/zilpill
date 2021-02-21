import math

# Got all the below addresses/info from https://viewblock.io/zilliqa

ZIL_API_URL = "https://api.zilliqa.com/"
# ZIL_API_URL = "https://ssn.zillet.io"

# Supply URL obtained from coingecko's zil page
ZIL_SUPPLY_URL = "https://stat.zilliqa.com/api/supply"

# Contracts
class CONTRACT:
    ZIL_SWAP_CONTRACT_ADD = "zil1hgg7k77vpgpwj3av7q7vv5dl4uvunmqqjzpv2w"
    ZILLION_CONTRACT_PROXY_ADD = "zil1g029nmzsf36r99vupp4s43lhs40fsscx3jjpuy"
    ZILLION_CONTRACT_ADD = "zil1k7qwsz2m3w595u29je0dvv4nka62c5wwrp8r8p"


# Token Contracts
class TOKEN:
    GZIL_BECH32_ADD = 'zil14pzuzq6v6pmmmrfjhczywguu0e97djepxt8g3e'
    XSGD_BECH32_PROXY_ADD = 'zil1zu72vac254htqpg3mtywdcfm84l3dfd9qzww8t'


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

