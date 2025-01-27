#!/usr/bin/env python3
import csv
import argparse
import os
import json
import sys
import datetime
import subprocess
import config

# Constants
MAX_MESSAGES_PER_TX = 333  # Based on maximum gas limit
FEE_DENOM = "ustars"       # Fee denomination for Stargaze
FEE_AMOUNT = "50000000"      # Fee amount in ustars
GAS_LIMIT = "50000000"     # Gas limit per transaction
FIXED_AMOUNT = 222

# Get the absolute path of the script directory
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

# Function to resolve absolute paths
def resolve_path(path):
    return os.path.abspath(os.path.join(SCRIPT_DIR, path))

def convert_to_micro_units(amount):
    """Convert standard units to micro units."""
    return int(amount * config.CONVERSION_RATE)

def main():
    parser = argparse.ArgumentParser(description="Generate transactions from CSV.")
    parser.add_argument("--csv", type=str, required=True,
                        help="Path to the CSV file with wallet addresses.")
    parser.add_argument("--from-address", type=str, required=True,
                        help="Sender's wallet address.")
    parser.add_argument("--denom", type=str, default=config.get_full_denom(config.DENOM),
                        help="Denomination of the token.")
    args = parser.parse_args()

    # Resolve paths
    csv_file_path = resolve_path(args.csv)
    transactions_dir = resolve_path("transactions")

    # Ensure the transactions directory exists
    os.makedirs(transactions_dir, exist_ok=True)

    # Check if CSV file exists
    if not os.path.isfile(csv_file_path):
        print(f"Error: CSV file '{csv_file_path}' does not exist.")
        sys.exit(1)

    # Read the CSV file with 'utf-8-sig' encoding to handle BOM
    with open(csv_file_path, 'r', encoding='utf-8-sig') as csvfile:
        lines = csvfile.read().splitlines()

        # Extract addresses from the CSV (skip the header)
        header = lines[0].strip().lower()
        if header != "address":
            print("Error: CSV file must contain a single column with the header 'address'.")
            sys.exit(1)
        addresses = [line.strip() for line in lines[1:]]

    # Convert the fixed amount to micro units
    micro_amount = convert_to_micro_units(FIXED_AMOUNT)

    messages = []
    transaction_counter = 0
    all_transactions = []

    for idx, address in enumerate(addresses):
        if not address:
            print(f"Skipping empty address at line {idx + 2}.")
            continue

        # Create the message for Stargaze
        msg = {
            "@type": "/cosmos.bank.v1beta1.MsgSend",
            "from_address": args.from_address,
            "to_address": address,
            "amount": [
                {
                    "denom": args.denom,
                    "amount": str(micro_amount)
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
