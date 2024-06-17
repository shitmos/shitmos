import pandas as pd
import json
import os
import subprocess
import config

# Define the directory paths
DATA_DIR = '../data'
ADDRESS_FILE = os.path.join(DATA_DIR, 'snapshots/clout_addresses.csv')
TRANSACTIONS_DIR = '../data/transactions'

# Create the transactions directory if it doesn't exist
os.makedirs(TRANSACTIONS_DIR, exist_ok=True)

# Load address data from CSV file
df = pd.read_csv(ADDRESS_FILE)

# Ensure all addresses are in lowercase
df['address'] = df['address'].apply(lambda x: x[0].lower() + x[1:] if x[0].isupper() else x)

def truncate(value, decimals):
    factor = 10.0 ** decimals
    return int(value * factor) / factor

def generate_transaction(df, unit_amount, common_denom, from_address):
    # Fetch the full denomination from the mapping
    full_denom = next((key for key, value in config.TOKEN_NAME_MAPPING.items() if value == common_denom), common_denom)
    fee_denom = "uosmo"
    fee_amount = "13500"
    gas_limit = "4500000"
    messages = []
    
    for _, row in df.iterrows():
        osmosis_address = row['address']
        amount = truncate(unit_amount * config.CONVERSION_RATE, 0)
        messages.append({
            "@type": "/cosmos.bank.v1beta1.MsgSend",
            "from_address": from_address,
            "to_address": osmosis_address,
            "amount": [
                {
                    "denom": full_denom,
                    "amount": str(int(amount))
                }
            ]
        })

    transaction = {
        "body": {
            "messages": messages,
            "memo": ""
        },
        "auth_info": {
            "signer_infos": [],
            "fee": {
                "amount": [
                    {
                        "denom": fee_denom,
                        "amount": fee_amount
                    }
                ],
                "gas_limit": gas_limit
            }
        },
        "signatures": []
    }

    return transaction

def save_transaction(transaction):
    timestamp = subprocess.check_output(['date', '+%Y%m%d_%H%M%S']).decode('utf-8').strip()
    transaction_file = os.path.join(TRANSACTIONS_DIR, f'transaction_{timestamp}.json')

    with open(transaction_file, 'w') as file:
        json.dump(transaction, file, indent=2)

    return transaction_file

def main():
    common_denom = config.DENOM
    unit_amount = config.UNIT_AMOUNT  # Use the value from the config file
    from_address = subprocess.check_output(
        ["osmosisd", "keys", "show", config.KEY_NAME, "-a", "--keyring-backend", "file"]
    ).decode("utf-8").strip()

    transaction = generate_transaction(df, unit_amount, common_denom, from_address)
    transaction_file = save_transaction(transaction)
    print(transaction_file)

if __name__ == "__main__":
    main()
