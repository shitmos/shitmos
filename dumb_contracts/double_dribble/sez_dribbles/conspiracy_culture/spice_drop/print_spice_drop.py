#!/usr/bin/env python3
import argparse
import os
import csv
import sys

# Adjust the path if config.py is in a different directory
# Replace 'path_to_config_directory' with the actual path to your config.py
script_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.abspath(os.path.join(script_dir, 'path_to_config_directory'))
sys.path.append(config_path)

try:
    import config
except ImportError:
    print("Error: Unable to import config.py. Please ensure it's in the specified directory.")
    sys.exit(1)

def truncate(value, decimals):
    """Truncate a value to a specified number of decimal places."""
    factor = 10.0 ** decimals
    return int(value * factor) / factor

def read_distribution_csv(csv_file):
    """Read the CSV file and return a list of distributions."""
    distributions = []
    total_distribution = 0.0
    total_wallets = 0

    if not os.path.isfile(csv_file):
        print(f"CSV file '{csv_file}' does not exist.")
        return distributions, total_distribution, total_wallets

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            wallet_address = row.get('wallet_address', '').strip()
            amount_str = row.get('amount', '').strip()
            if not wallet_address or not amount_str:
                continue
            try:
                amount = float(amount_str)
            except ValueError:
                print(f"Invalid amount '{amount_str}' for wallet '{wallet_address}' in CSV.")
                continue
            distributions.append({'wallet_address': wallet_address, 'amount': amount})
            total_distribution += amount
            total_wallets += 1

    return distributions, total_distribution, total_wallets

def calculate_and_print_distributions(distributions, denom):
    output = []
    total_distribution = 0.0
    total_wallets = 0

    output.append("\nSpice Drop Distribution:")
    output.append("-" * 80)
    output.append("{:<6} {:<44} {:<15} {:<10}".format("No.", "Wallet Address", "Amount", "Denom"))
    output.append("-" * 80)

    for idx, dist in enumerate(distributions, start=1):
        wallet_address = dist['wallet_address']
        amount = dist['amount']
        total_distribution += amount
        total_wallets += 1
        output.append("{:<6} {:<44} {:<15.2f} {:<10}".format(idx, wallet_address, amount, denom))

    total_distribution = round(total_distribution, 2)
    output.append("-" * 80)
    output.append(f"Total distribution: {total_distribution:.2f} {denom}")
    output.append(f"Total number of wallets: {total_wallets}")
    output.append("-" * 80)

    # Print the entire collected output once
    print("\n".join(output))

def main():
    parser = argparse.ArgumentParser(description="Print Spice Drop distribution details.")
    parser.add_argument("--csv-file", type=str, default="distribution.csv",
                        help="The CSV file containing wallet addresses and amounts.")
    parser.add_argument("--denom", type=str, default=config.DENOM,
                        help="The token denomination to use for distributions.")

    args = parser.parse_args()

    distributions, total_distribution, total_wallets = read_distribution_csv(args.csv_file)
    if not distributions:
        print("No distributions found.")
        return

    calculate_and_print_distributions(distributions, args.denom)

if __name__ == "__main__":
    main()
