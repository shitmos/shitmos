# print_shitdribble.py
import json
import os
import argparse
import config

# Define the directory paths
DATA_DIR = '../data'
COLLECTIONS_FILE = os.path.join(DATA_DIR, 'collections.json')
CONVERTED_ADDRESSES_FILE = os.path.join(DATA_DIR, 'converted_addresses.json')

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

def calculate_and_print_distributions(collections, unit_amount, denom):
    output = []
    output.append(f"{'Collection':<20} {'Recipient Name':<30} {'Weight':<10} {'Amount':<15} {'Denom':<10} {'Osmosis Address':<50}")
    output.append("-" * 140)

    total_amount = 0
    
    for collection in collections:
        name = collection['name']
        recipients = collection['recipients']
        total_weight = sum(recipient['weight'] for recipient in recipients)
        
        for recipient in recipients:
            recipient_name = recipient['label']
            weight = recipient['weight']
            amount = truncate((weight / total_weight) * unit_amount, 2)
            total_amount += amount
            osmosis_address = address_mapping.get(recipient_name, 'Unknown')
            output.append(f"{name:<30} {recipient_name:<30} {weight:<10} {amount:<15.2f} {denom:<10} {osmosis_address:<50}")


    output.append("-" * 140)
    output.append(f"{'Total':<71} {total_amount:<15.2f} {denom:<10}")
    output.append("-" * 140)
    output.append("")
    
    # Print the entire collected output once
    print("\n".join(output))

def main():
    parser = argparse.ArgumentParser(description="Calculate and print distribution details.")
    parser.add_argument("--denom", type=str, default=config.DENOM, help="The token denomination to distribute.")
    parser.add_argument("--amount", type=float, default=config.UNIT_AMOUNT, help="The unit amount to distribute to each collection.")

    args = parser.parse_args()
    
    collections = collections_data['collections']
    calculate_and_print_distributions(collections, args.amount, args.denom)

if __name__ == "__main__":
    main()
