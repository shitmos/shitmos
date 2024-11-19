# config.py

# Wallet KEY_NAMES:
# shitmos_nft = Shitmos NFT Wallet
# sez = Shitmos Economic Zone Wallet

# Wallet Name
KEY_NAME = "sez"
WALLET_NAME = "Shitmos Economic Zone Wallet"

# Denomination configuration
# Set the common name of the token
DENOM = "AKT"

# Define conversion rate (1 unit = 1,000,000 micro units)
CONVERSION_RATE = 1_000_000

# Define a mapping from full token denominations to common names
TOKEN_NAME_MAPPING = {
    "uosmo": "OSMO",
    "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/crazyhorse": "CRAZYHORSE",
    "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/cwad": "CWAD",
    "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/shitmos": "SHITMOS",
    "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/pnt": "PNT",
    "ibc/987C17B11ABC2B20019178ACE62929FE9840202CE79498E29FE8E5CB02B7C0A4": "RSTK",
    "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/crmh": "CRMH",
    "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/bag": "BAG",
    "ibc/1480B8FD20AD5FCAE81EA87584D269547DD4D436843C1D20F15E00EB64743EF4": "AKT",
}

# Define a reverse mapping from common names to full denominations
COMMON_NAME_TO_DENOM = {v: k for k, v in TOKEN_NAME_MAPPING.items()}

# Function to get full denom from common name
def get_full_denom(common_name):
    return COMMON_NAME_TO_DENOM.get(common_name.upper(), common_name)

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

# Path to the distribution CSV file
DISTRIBUTION_CSV_FILE = "../snapshots/2024-11-18/spice_drop_2.csv"  # Update this if the file is located elsewhere

# Column names in the distribution CSV file
CSV_WALLET_COLUMN = "wallet"  # The header for the wallet addresses
CSV_AMOUNT_COLUMN = "airdrop_amount"  # The header for the distribution amounts