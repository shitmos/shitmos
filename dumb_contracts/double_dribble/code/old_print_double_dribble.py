#!/usr/bin/env python3
import json
import os
import argparse
import config
import pandas as pd
from config import SNAPSHOT_FILE

# Define the directory paths
DATA_DIR = '../data'

# Load snapshot data from CSV file
df = pd.read_csv(SNAPSHOT_FILE)

def truncate(value, decimals):
    factor = 10.0 ** decimals
    return int(value * factor) / factor

def calculate_and_print_distributions(df, unit_amount, denom):
    output = []
    output.append(f"{'Address':<50} {'Amount':<15} {'Denom':<10}")
    output.append("-" * 75)

    total_amount = 0

    for index, row in df.iterrows():
        address = row['address']
        amount = truncate(row['amount'] * unit_amount, 2)
        total_amount += amount
        output.append(f"{address:<50} {amount:<15.2f} {denom:<10}")

    output.append("-" * 75)
    output.append(f"{'Total':<50} {total_amount:<15.2f} {denom:<10}")
    output.append("-" * 75)
    output.append("")

    # Print the entire collected output once
    print("\n".join(output))

def main():
    parser = argparse.ArgumentParser(description="Calculate and print distribution details.")
    parser.add_argument("--denom", type=str, default=config.DENOM, help="The token denomination to distribute.")
    parser.add_argument("--amount", type=float, default=config.UNIT_AMOUNT, help="The unit amount to distribute to each address.")

    args = parser.parse_args()
    
    calculate_and_print_distributions(df, args.amount, args.denom)

if __name__ == "__main__":
    main()
