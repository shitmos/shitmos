# config.py
# wallet KEY_NAMES:
# shitmos_nft = Shitmos NFT Wallet
# sez = Shitmos Economic Zone Wallet


# Snapshot
SNAPSHOTS_FOLDER = "../sez_dribbles/conspiracy_culture/snapshots"
INCLUDE_LISTED_NFT_FOR_DISTRIBUTE = True

# Wallet Name
KEY_NAME = "sez"
WALLET_NAME = "Shitmos Economic Zone Wallet"

# Denomination and amount configuration
DENOM = "SHITMOS"
UNIT_AMOUNT = 22.22

# Define conversion rate (1 unit = 1,000,000 micro units)
CONVERSION_RATE = 1_000_000

# Define a mapping from token denominations to common names
TOKEN_NAME_MAPPING = {
    "uosmo": "OSMO",
    "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/crazyhorse": "CRAZYHORSE",
    "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/cwad": "CWAD",
    "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/shitmos": "SHITMOS",
    "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/pnt": "PNT",
    "ibc/987C17B11ABC2B20019178ACE62929FE9840202CE79498E29FE8E5CB02B7C0A4": "RSTK",
    "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/crmh": "CRMH",
    "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/bag": "BAG"
}

# Define exchange rates to USD (example rates)
EXCHANGE_RATES = {
    "OSMO": 0.87487, 
    "CRAZYHORSE": 0.0046809,
    "CWAD": 0.001026,
    "SHITMOS": 0.020357,
    "PNT": 0.001,
}

# Default exchange rate for unrecognized denominations
DEFAULT_EXCHANGE_RATE = 1.00
