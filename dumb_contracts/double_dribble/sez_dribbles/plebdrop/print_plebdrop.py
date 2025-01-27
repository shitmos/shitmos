#!/usr/bin/env python3
import argparse
import csv
import os
import datetime

# Fixed amount of PLEB to distribute
FIXED_AMOUNT = 222

def main():
    parser = argparse.ArgumentParser(description="Print PLEBDROP distribution summary.")
    parser.add_argument("--csv-file", type=str, required=True,
                        help="Path to the CSV file with wallet addresses.")
    parser.add_argument("--denom", type=str, required=True,
                        help="Denomination of the token.")
    parser.add_argument("--transaction-count", type=int, required=True,
                        help="Number of transactions generated.")
    args = parser.parse_args()

    # Check if CSV file exists
    if not os.path.isfile(args.csv_file):
        print(f"Error: CSV file '{args.csv_file}' does not exist.")
        return

    # Read addresses from the CSV file
    with open(args.csv_file, 'r', encoding='utf-8-sig') as csvfile:
        lines = csvfile.read().splitlines()

        # Validate the header
        header = lines[0].strip().lower()
        if header != "address":
            print("Error: CSV file must contain a single column with the header 'address'.")
            return

        # Count valid addresses
        addresses = [line.strip() for line in lines[1:] if line.strip()]
        wallet_count = len(addresses)

    # Calculate total amount distributed
    total_amount = wallet_count * FIXED_AMOUNT

    # Print the distribution summary
    print("\nPLEBDROP Distribution Summary:")
    print("-" * 80)
    print(f"{'Wallets':<20}{'Amount per Wallet':<30}{'Total Amount Sent':<30}")
    print("-" * 80)
    print(f"{wallet_count:<20}{FIXED_AMOUNT:<30}{total_amount:<30}")
    print("-" * 80)
    print(f"Total {args.denom} Sent: {total_amount}")
    print(f"Total Wallets: {wallet_count}")
    print(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}")
    print(f"Number of Transactions: {args.transaction_count}")
    print("-" * 80)

if __name__ == "__main__":
    main()
