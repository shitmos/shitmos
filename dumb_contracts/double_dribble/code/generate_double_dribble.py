import pandas as pd
import json
import os
import subprocess
import bech32
import config
from snapshots import calculate_holders

# Define constants
MAX_MESSAGES_PER_TX = 333  # Based on maximum gas limit
DATA_DIR = '../data'
TRANSACTIONS_DIR = '../data/transactions'

# Create the transactions directory if it doesn't exist
os.makedirs(TRANSACTIONS_DIR, exist_ok=True)


def convert_address(stargaze_address, target_prefix="osmo"):
    """
    Convert a Stargaze address to an Osmosis address.
    """
    hrp, data = bech32.bech32_decode(stargaze_address)
    osmosis_address = bech32.bech32_encode(target_prefix, data)
    return osmosis_address


def truncate(value, decimals):
    factor = 10.0 ** decimals
    return int(value * factor) / factor


def generate_transactions(holders_counted, unit_amount, common_denom, from_address):
    full_denom = next((key for key, value in config.TOKEN_NAME_MAPPING.items() if value == common_denom), common_denom)
    fee_denom = "uosmo"
    fee_amount = "26768"
    gas_limit = "8655946"
    all_transactions = []
    messages = []

    for stargaze_address, nft_count in holders_counted.items():
        osmosis_address = convert_address(stargaze_address)
        amount = truncate(nft_count * unit_amount * config.CONVERSION_RATE, 0)
        
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

        # When the number of messages reaches the max, create a new transaction
        if len(messages) >= MAX_MESSAGES_PER_TX:
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
            all_transactions.append(transaction)
            messages = []

    # Add remaining messages as the last transaction
    if messages:
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
        all_transactions.append(transaction)

    return all_transactions


def save_transaction(transaction, index):
    timestamp = subprocess.check_output(['date', '+%Y%m%d_%H%M%S']).decode('utf-8').strip()
    transaction_file = os.path.join(TRANSACTIONS_DIR, f'transaction_{index}_{timestamp}.json')

    with open(transaction_file, 'w') as file:
        json.dump(transaction, file, indent=2)

    return transaction_file


def main():
    common_denom = config.DENOM
    unit_amount = config.UNIT_AMOUNT
    from_address = subprocess.check_output(
        ["osmosisd", "keys", "show", config.KEY_NAME, "-a", "--keyring-backend", "file"]
    ).decode("utf-8").strip()

    holders_counted = calculate_holders(include_listed=config.INCLUDE_LISTED_NFT_FOR_DISTRIBUTE)
    transactions = generate_transactions(holders_counted, unit_amount, common_denom, from_address)

    for index, transaction in enumerate(transactions):
        transaction_file = save_transaction(transaction, index)
        print(f"Transaction {index + 1}/{len(transactions)} saved: {transaction_file}")


if __name__ == "__main__":
    main()
