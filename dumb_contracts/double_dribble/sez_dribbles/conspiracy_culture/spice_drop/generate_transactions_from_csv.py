import csv
import argparse
import os
import json

parser = argparse.ArgumentParser(description='Generate transactions from CSV.')
parser.add_argument('--csv', required=True, help='Path to the CSV file with wallet addresses and amounts.')
parser.add_argument('--from-address', required=True, help='Sender\'s wallet address.')
parser.add_argument('--denom', required=True, help='Denomination of the token.')
args = parser.parse_args()

TRANSACTIONS_DIR = "../data/transactions"

# Ensure the transactions directory exists
os.makedirs(TRANSACTIONS_DIR, exist_ok=True)

with open(args.csv, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for idx, row in enumerate(reader):
        to_address = row['wallet_address'].strip()
        amount_str = row['amount'].strip()
        try:
            # Convert amount to micro units (assuming the amount is in whole units)
            amount = int(float(amount_str) * 1e6)
        except ValueError:
            print(f"Invalid amount '{amount_str}' for wallet '{to_address}' in CSV.")
            continue

        tx = {
            "body": {
                "messages": [
                    {
                        "@type": "/cosmos.bank.v1beta1.MsgSend",
                        "from_address": args.from_address,
                        "to_address": to_address,
                        "amount": [
                            {
                                "denom": args.denom,
                                "amount": str(amount)
                            }
                        ]
                    }
                ],
                "memo": "",
                "timeout_height": "0",
                "extension_options": [],
                "non_critical_extension_options": []
            },
            "auth_info": {
                "signer_infos": [],
                "fee": {
                    "amount": [],
                    "gas_limit": "200000",
                    "payer": "",
                    "granter": ""
                }
            },
            "signatures": []
        }
        json_file = os.path.join(TRANSACTIONS_DIR, f"transaction_{idx}.json")
        with open(json_file, 'w') as f:
            json.dump(tx, f, indent=4)
        print(f"Transaction saved: {json_file}")
