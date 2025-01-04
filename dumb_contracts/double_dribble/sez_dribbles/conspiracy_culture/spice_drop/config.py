# config.py

# Wallet KEY_NAMES:
# shitmos_nft = Shitmos NFT Wallet
# sez = Shitmos Economic Zone Wallet
# shitmos = Shitmos Hot Wallet

# Wallet Name
KEY_NAME = "shitmos"
WALLET_NAME = "Shitmos Economic Zone Wallet"

# Denomination configuration
# Set the common name of the token
DENOM = "CRBRUS"

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
    "ibc/41999DF04D9441DAC0DF5D8291DF4333FBCBA810FFD63FDCE34FDF41EF37B6F7": "CRBRUS",
    "ibc/FE2CD1E6828EC0FAB8AF39BAC45BC25B965BA67CCBC50C13A14BD610B0D1E2C4": "BOOT",
}

# Define a reverse mapping from common names to full denominations
COMMON_NAME_TO_DENOM = {v: k for k, v in TOKEN_NAME_MAPPING.items()}

# Function to get full denom from common name
def get_full_denom(common_name):
    return COMMON_NAME_TO_DENOM.get(common_name.upper(), common_name)


# Default exchange rate for unrecognized denominations
DEFAULT_EXCHANGE_RATE = 1.00

# Path to the distribution CSV file
DISTRIBUTION_CSV_FILE = "../../plebdrop/snapshots/nice_list_osmo.csv"  # Update this if the file is located elsewhere

# Column names in the distribution CSV file
CSV_WALLET_COLUMN = "address"  # The header for the wallet addresses
CSV_AMOUNT_COLUMN = "CRBRUS"  # The header for the distribution amounts