# config.py

# Wallet KEY_NAME:
# Specify the wallet key name for Stargaze
KEY_NAME = "shitmos"
WALLET_NAME = "Shitmos Economic Zone Wallet"

# Denomination configuration
# Denomination used on Stargaze
DENOM = "factory/stars1k7qsxdxh8calmt4txk75e6hdntefslegwddqnlwjjqgjkmcfqy0qa97sn8/pleb"

# Conversion rate (1 unit = 1,000,000 micro units)
CONVERSION_RATE = 1_000_000

# Define a mapping from full token denominations to common names
TOKEN_NAME_MAPPING = {
    "ustars": "STARS",
    "factory/stars1k7qsxdxh8calmt4txk75e6hdntefslegwddqnlwjjqgjkmcfqy0qa97sn8/pleb": "PLEB",
    "ibc/8577E98BDDD2758FD5647A53563DAAC89921326F964EBF899B945ED05A66CA5F":"SHITMOS",
}

# Define a reverse mapping from common names to full denominations
COMMON_NAME_TO_DENOM = {v: k for k, v in TOKEN_NAME_MAPPING.items()}

# Function to get full denom from common name
def get_full_denom(common_name):
    return COMMON_NAME_TO_DENOM.get(common_name.upper(), common_name)

# Path to the distribution CSV file
DISTRIBUTION_CSV_FILE = "snapshots/naughty_list.csv"  # Update this path as needed

# Column names in the distribution CSV file
CSV_WALLET_COLUMN = "address"  # Header for wallet addresses
CSV_AMOUNT_COLUMN = "PLEB"  # Header for distribution amounts
