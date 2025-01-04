# config.py

# Wallet KEY_NAME:
# Specify the wallet key name for Stargaze
KEY_NAME = "shitmos"
WALLET_NAME = "Shitmos Economic Zone Wallet"

# Denomination configuration
# Denomination used on Stargaze
DENOM = "ustars"

# Conversion rate (1 unit = 1,000,000 micro units)
CONVERSION_RATE = 1_000_000

# Define a mapping from full token denominations to common names
TOKEN_NAME_MAPPING = {
    "ustars": "STARS",
    "factory/stars1k7qsxdxh8calmt4txk75e6hdntefslegwddqnlwjjqgjkmcfqy0qa97sn8/pleb": "PLEB",
}

# Define a reverse mapping from common names to full denominations
COMMON_NAME_TO_DENOM = {v: k for k, v in TOKEN_NAME_MAPPING.items()}

# Function to get full denom from common name
def get_full_denom(common_name):
    return COMMON_NAME_TO_DENOM.get(common_name.upper(), common_name)

# Path to the distribution CSV file
DISTRIBUTION_CSV_FILE = "../../plebdrop/stars_airdrop.csv"  # Update this path as needed

# Column names in the distribution CSV file
CSV_WALLET_COLUMN = "wallet"  # Header for wallet addresses
CSV_AMOUNT_COLUMN = "airdrop_amount"  # Header for distribution amounts
