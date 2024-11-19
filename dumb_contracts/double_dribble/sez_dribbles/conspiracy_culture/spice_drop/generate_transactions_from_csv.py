#!/usr/bin/env python3
import csv
import argparse
import os
import json
import sys
import datetime
import subprocess
import config
import bech32  # Ensure bech32 is imported

# Constants
MAX_MESSAGES_PER_TX = 333  # Based on maximum gas limit
FEE_DENOM = "uosmo"        # Fee denomination
FEE_AMOUNT = "45000"       # Fee amount in uosmo
GAS_LIMIT = "15000000"     # Gas limit per transaction

# Get the absolute path of the script directory
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

def convert_address(stargaze_address, target_prefix="osmo"):
    """
    Convert a Stargaze address to an Osmosis address.
    """
    hrp, data = bech32.bech32_decode(stargaze_address)
    if data is None:
        print(f"Invalid Stargaze address: {stargaze_address}")
        return None
    osmosis_address = bech32.bech32_encode(target_prefix, data)
    return osmosis_address

# Function to resolve absolute paths
def resolve_path(path):
    return os.path.abspath(os.path.join(SCRIPT_DIR, path))

def main():
    parser = argparse.ArgumentParser(description='Generate transactions from CSV.')
    parser.add_argument('--csv', type=str, default=config.DISTRIBUTION_CSV_FILE,
                        help='Path to the CSV file with wallet addresses and amounts.')
    parser.add_argument('--from-address', type=str, required=False,
                        help='Sender\'s wallet address.')
    parser.add_argument('--denom', type=str, default=config.get_full_denom(config.DENOM),
                        help='Denomination of the token.')
    args = parser.parse_args()

    # Get from_address if not provided
    if not args.from_address:
        args.from_address = subprocess.check_output(
            ["osmosisd", "keys", "show", config.KEY_NAME, "-a", "--keyring-backend", "file"]
        ).decode("utf-8").strip()

    # Resolve paths
    csv_file_path = resolve_path(args.csv)
    transactions_dir = resolve_path("../data/transactions")

    # Ensure the transactions directory exists
    os.makedirs(transactions_dir, exist_ok=True)

    # Check if CSV file exists
    if not os.path.isfile(csv_file_path):
        print(f"Error: CSV file '{csv_file_path}' does not exist.")
        sys.exit(1)

    # Read the CSV file with 'utf-8-sig' encoding to handle BOM
    with open(csv_file_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        print(f"CSV headers detected: {reader.fieldnames}")  # Debug statement

        # Verify that the required columns are present
        if config.CSV_WALLET_COLUMN not in reader.fieldnames or config.CSV_AMOUNT_COLUMN not in reader.fieldnames:
            print(f"Error: CSV file does not contain required columns '{config.CSV_WALLET_COLUMN}' and '{config.CSV_AMOUNT_COLUMN}'.")
            sys.exit(1)

        messages = []
        transaction_counter = 0
        all_transactions = []

        for idx, row in enumerate(reader):
            stargaze_address = row.get(config.CSV_WALLET_COLUMN, '').strip()
            amount_str = row.get(config.CSV_AMOUNT_COLUMN, '').strip()

            if not stargaze_address:
                print(f"Missing wallet address in row {idx}.")
                continue
            if not amount_str:
                print(f"Missing amount in row {idx} for wallet '{stargaze_address}'.")
                continue

            try:
                # Convert amount to micro units using CONVERSION_RATE
                amount = int(float(amount_str) * config.CONVERSION_RATE)
            except ValueError:
                print(f"Invalid amount '{amount_str}' for wallet '{stargaze_address}' in row {idx}.")
                continue

            # Convert the Stargaze address to an Osmosis address
            osmosis_address = convert_address(stargaze_address)
            if osmosis_address is None:
                print(f"Skipping invalid address at row {idx}: {stargaze_address}")
                continue

            # Create the message with the converted address
            msg = {
                "@type": "/cosmos.bank.v1beta1.MsgSend",
                "from_address": args.from_address,
                "to_address": osmosis_address,
                "amount": [
                    {
                        "denom": args.denom,
                        "amount": str(amount)
                    }
                ]
            }
            messages.append(msg)

            # When the number of messages reaches the max, create a new transaction
            if len(messages) >= MAX_MESSAGES_PER_TX:
                transaction = create_transaction(messages)
                all_transactions.append(transaction)
                print(f"Transaction {transaction_counter} created with {len(messages)} messages.")
                save_transaction(transaction, transaction_counter, transactions_dir)
                messages = []
                transaction_counter += 1

        # Add remaining messages as the last transaction
        if messages:
            transaction = create_transaction(messages)
            all_transactions.append(transaction)
            print(f"Transaction {transaction_counter} created with {len(messages)} messages.")
            save_transaction(transaction, transaction_counter, transactions_dir)
            transaction_counter += 1

        print(f"Total transactions created: {transaction_counter}")

def create_transaction(messages):
    tx = {
        "body": {
            "messages": messages,
            "memo": "",
            "timeout_height": "0",
            "extension_options": [],
            "non_critical_extension_options": []
        },
        "auth_info": {
            "signer_infos": [],
            "fee": {
                "amount": [
                    {
                        "denom": FEE_DENOM,
                        "amount": FEE_AMOUNT
                    }
                ],
                "gas_limit": GAS_LIMIT,
                "payer": "",
                "granter": ""
            }
        },
        "signatures": []
    }
    return tx

def save_transaction(transaction, index, transactions_dir):
    date_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    json_file = os.path.join(transactions_dir, f"transaction_{date_str}_{index:04d}.json")
    with open(json_file, 'w') as f:
        json.dump(transaction, f, indent=4)
    print(f"Transaction saved: {json_file}")

if __name__ == "__main__":
    main()
