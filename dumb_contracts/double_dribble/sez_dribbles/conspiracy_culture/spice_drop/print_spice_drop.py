#!/usr/bin/env python3
import argparse
import os
import csv
import sys
import config
from datetime import datetime
from collections import defaultdict

def read_distribution_csv(csv_file):
    """Read the CSV file and return a list of distributions."""
    distributions = []
    total_distribution = 0.0
    total_wallets = 0

    if not os.path.isfile(csv_file):
        print(f"CSV file '{csv_file}' does not exist.")
        return distributions

    with open(csv_file, 'r', newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        if config.CSV_WALLET_COLUMN not in reader.fieldnames or config.CSV_AMOUNT_COLUMN not in reader.fieldnames:
            print(f"Error: CSV file does not contain required columns '{config.CSV_WALLET_COLUMN}' and '{config.CSV_AMOUNT_COLUMN}'.")
            sys.exit(1)

        for row in reader:
            wallet_address = row.get(config.CSV_WALLET_COLUMN, '').strip()
            amount_str = row.get(config.CSV_AMOUNT_COLUMN, '').strip()
            nfts_held = row.get('nfts_held', '').strip()
            if not wallet_address or not amount_str:
                continue
            try:
                amount = float(amount_str)
            except ValueError:
                print(f"Invalid amount '{amount_str}' for wallet '{wallet_address}' in CSV.")
                continue
            distributions.append({'wallet_address': wallet_address, 'amount': amount, 'nfts_held': nfts_held})
            total_distribution += amount
            total_wallets += 1

    return distributions

def summarize_distributions(distributions):
    summary = defaultdict(lambda: {'wallets': 0, 'total_amount': 0.0})
    total_amount_sent = 0.0
    total_wallets = len(distributions)

    for dist in distributions:
        nfts_held = dist.get('nfts_held', 'Unknown')
        amount = dist['amount']
        summary[nfts_held]['wallets'] += 1
        summary[nfts_held]['amount_per_wallet'] = amount  # Assuming same amount per wallet per NFTs held
        summary[nfts_held]['total_amount'] += amount
        total_amount_sent += amount

    return summary, total_amount_sent, total_wallets

def print_distribution_summary(summary, total_amount_sent, total_wallets, transaction_count, denom):
    date_today = datetime.now().strftime('%Y-%m-%d')
    print("\nDistribution Summary:")
    print("-" * 80)
    print("{:<15} {:<15} {:<25} {:<20}".format("NFTs Held", "Wallets", f"Amount per Wallet ({denom})", f"Total {denom} Sent"))
    print("-" * 80)
    for nfts_held, data in summary.items():
        print("{:<15} {:<15} {:<25.2f} {:<20.2f}".format(
            nfts_held, data['wallets'], data['amount_per_wallet'], data['total_amount']
        ))
    print("-" * 80)
    print(f"Total {denom} Sent: {total_amount_sent:.2f}")
    print(f"Total Wallets: {total_wallets}")
    print(f"Date: {date_today}")
    print(f"Number of Transactions: {transaction_count}")
    print("-" * 80)

def main():
    parser = argparse.ArgumentParser(description="Print Spice Drop distribution details.")
    parser.add_argument("--csv-file", type=str, default=config.DISTRIBUTION_CSV_FILE,
                        help="The CSV file containing wallet addresses and amounts.")
    parser.add_argument("--denom", type=str, default=config.DENOM,
                        help="The token denomination to use for distributions.")
    parser.add_argument("--transaction-count", type=int, default=1,
                        help="The number of transactions used.")
    args = parser.parse_args()

    distributions = read_distribution_csv(args.csv_file)
    if not distributions:
        print("No distributions found.")
        return

    summary, total_amount_sent, total_wallets = summarize_distributions(distributions)
    print_distribution_summary(summary, total_amount_sent, total_wallets, args.transaction_count, args.denom)

if __name__ == "__main__":
    main()
