# config.py

# Wallet Name


# Denomination and amount configuration
DENOM = "SHITMOS"
UNIT_AMOUNT = 22.0

# Define conversion rate (1 unit = 1,000,000 micro units)
CONVERSION_RATE = 1_000_000

# Define a mapping from token denominations to common names
TOKEN_NAME_MAPPING = {
    "uosmo": "OSMO",
    "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/crazyhorse": "CRAZYHORSE",
    "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/cwad": "CWAD",
    "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/shitmos": "SHITMOS"
}

# Define exchange rates to USD (example rates)
EXCHANGE_RATES = {
    "OSMO": 0.87487, 
    "CRAZYHORSE": 0.0046809,
    "CWAD": 0.001026,
    "SHITMOS": 0.020357
}

# Default exchange rate for unrecognized denominations
DEFAULT_EXCHANGE_RATE = 1.00
