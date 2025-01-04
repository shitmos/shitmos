import pandas as pd
import subprocess

# Wallet Key Name for both blockchains
KEY_NAME = "shitmos"

# Default Denominations and Conversion Rates
BLOCKCHAIN_SETTINGS = {
    "osmosis": {
        "denom": "uosmo",
        "fee_denom": "uosmo",
        "fee_amount": "45000",  # in micro-units
        "gas_limit": "15000000",  # gas per transaction
    },
    "stargaze": {
        "denom": "ustars",
        "fee_denom": "ustars",
        "fee_amount": "20000",  # in micro-units
        "gas_limit": "10000000",  # gas per transaction
    },
}

# Conversion Rate (1 token = 1,000,000 micro-units)
CONVERSION_RATE = 1_000_000

# Max messages per transaction (for batching)
MAX_MESSAGES_PER_TX = 333

# Naughty list configuration
NAUGHTY_LIST_CSV_FILE = "snapshots/naughty_list.csv"
NAUGHTY_LIST_AMOUNT = 1  # Fixed amount per wallet in token units
NAUGHTY_LIST_TOKEN = "CRAZYHORSE"  # Token to send for naughty list

# Nice list configuration
NICE_LIST_CSV_FILE = "snapshots/nice_list.csv"
NICE_LIST_COLUMNS = {  # Columns specifying amounts for each token
    "SHITMOS": "SHITMOS",
    "CRBRUS": "CRBRUS",
    "PLEB": "PLEB",
}

# Default CSV Columns
CSV_WALLET_COLUMN = "address"  # Wallet address column
CSV_AMOUNT_COLUMN = "airdrop_amount"  # General-purpose amount column

# Token Mapping File
TOKEN_MAPPING_FILE = "token_mapping.csv"

# Function to fetch blockchain-specific settings
def get_blockchain_settings(blockchain):
    """
    Fetch the blockchain-specific settings from BLOCKCHAIN_SETTINGS.
    """
    return BLOCKCHAIN_SETTINGS.get(blockchain, {})


def load_token_mapping():
    """
    Load token mapping from the token_mapping.csv file.
    """
    try:
        df = pd.read_csv(TOKEN_MAPPING_FILE)
        return {
            row["denom"]: row["name"] if pd.notna(row["name"]) else row["denom"]
            for _, row in df.iterrows()
        }
    except Exception as e:
        print(f"Error loading token mapping: {e}")
        return {}


def get_full_denom(token_name, blockchain):
    """
    Retrieve the full denom from the token name and blockchain.
    Fallback to the token name if no mapping is found.
    """
    token_mapping = load_token_mapping()
    blockchain_settings = BLOCKCHAIN_SETTINGS.get(blockchain, {})
    return token_mapping.get(token_name, blockchain_settings.get("denom", token_name))


def get_sender_address(blockchain):
    """
    Fetch the sender's wallet address using the CLI tool for the blockchain.
    """
    cli_tool = "osmosisd" if blockchain == "osmosis" else "starsd"
    command = [cli_tool, "keys", "show", KEY_NAME, "-a"]
    try:
        import subprocess
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error fetching sender address for '{blockchain}': {e.stderr}")
        raise
