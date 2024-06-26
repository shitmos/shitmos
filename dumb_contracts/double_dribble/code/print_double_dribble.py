#!/usr/bin/env python3
import json
import os
import argparse
import config
import pandas as pd
from config import SNAPSHOT_FILE

# Load snapshot data from CSV file
df = pd.read_csv(SNAPSHOT_FILE)

def truncate(value, decimals):
    """ Truncate a value to a specified number of decimal places. """
    factor = 10.0 ** decimals
    return int(value * factor) / factor

def calculate_and_print_distributions(df, unit_amount, denom):
    # Group by the 'amount' column (number of NFTs held) and count each group
    grouped = df.groupby('amount').size().reset_index(name='count').sort_values('amount', ascending=False)

    # Calculate distribution for each group and total distribution
    output = []
    total_distribution = 0
    total_wallets = 0

    output.append("Double dribble distribution:")
    output.append("-" * 66)
    output.append("{:<6} {:<5} {:<12} {:<15} {:<10} {:<10}".format("Count", "NFTs", "💩 per NFT", "💩 Per Wallet", "Total", "Denom"))
    output.append("-" * 66)

    for index, row in grouped.iterrows():
        wallet_count = row['count']
        nft_count = row['amount']
        total_wallets += wallet_count
        distribution_per_wallet = truncate(nft_count * unit_amount, 2)
        total_for_group = truncate(wallet_count * distribution_per_wallet, 2)
        total_distribution += total_for_group

        output.append("{:<6} {:<5} {:<12.2f} {:<15.2f} {:<10.2f} {:<10}".format(wallet_count, nft_count, unit_amount, distribution_per_wallet, total_for_group, denom))

    total_distribution = round(total_distribution, 2)  # Round the total distribution to two decimal places
    output.append("-" * 66)
    output.append(f"Total distribution: {total_distribution}")
    output.append(f"Total number of wallets: {total_wallets}")

    # Print the entire collected output once
    print("\n".join(output))

def main():
    parser = argparse.ArgumentParser(description="Calculate and print NFT distribution details.")
    parser.add_argument("--amount", type=float, default=config.UNIT_AMOUNT, help="The unit amount to distribute to each address.")
    parser.add_argument("--denom", type=str, default=config.DENOM, help="The token denomination to use for distributions.")

    args = parser.parse_args()
    
    calculate_and_print_distributions(df, args.amount, args.denom)

if __name__ == "__main__":
    main()
