import json
import os
import subprocess
import config

# Define the directory paths
DATA_DIR = '../data'
COLLECTIONS_FILE = os.path.join(DATA_DIR, 'collections.json')
CONVERTED_ADDRESSES_FILE = os.path.join(DATA_DIR, 'converted_addresses.json')
TRANSACTIONS_DIR = '../data/transactions'

# Create the transactions directory if it doesn't exist
os.makedirs(TRANSACTIONS_DIR, exist_ok=True)

# Load collection data from JSON file
with open(COLLECTIONS_FILE, 'r') as file:
    collections_data = json.load(file)

# Load converted addresses data from JSON file
with open(CONVERTED_ADDRESSES_FILE, 'r') as file:
    converted_addresses_data = json.load(file)

# Create a mapping from recipient name to osmosis address
address_mapping = {recipient['name']: recipient['osmosis_address'] for recipient in converted_addresses_data['recipients']}

def truncate(value, decimals):
    factor = 10.0 ** decimals
    return int(value * factor) / factor

def generate_transaction(collections, unit_amount, common_denom, from_address):
    full_denom = {v: k for k, v in config.TOKEN_NAME_MAPPING.items()}[common_denom]
    fee_denom = "uosmo"  # Set the fee denom
    fee_amount = "5000"  # Set the fee amount (in micro units)
    gas_limit = "1000000"  # Increase the gas limit
    messages = []
    
    for collection in collections:
        recipients = collection['recipients']
        total_weight = sum(recipient['weight'] for recipient in recipients)
        
        for recipient in recipients:
            recipient_name = recipient['label']
            weight = recipient['weight']
            amount = truncate((weight / total_weight) * unit_amount, 2) * config.CONVERSION_RATE  # Convert to micro units
            osmosis_address = address_mapping.get(recipient_name, 'Unknown')
            if osmosis_address != 'Unknown':
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
    unit_amount = config.UNIT_AMOUNT
    from_address = subprocess.check_output(
        ["osmosisd", "keys", "show", "sez", "-a", "--keyring-backend", "file"]
    ).decode("utf-8").strip()

    collections = collections_data['collections']
    transaction = generate_transaction(collections, unit_amount, common_denom, from_address)
    transaction_file = save_transaction(transaction)
    print(transaction_file)

if __name__ == "__main__":
    main()
