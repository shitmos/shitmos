import os
import json
import csv
from collections import Counter
from datetime import datetime

# Input variables at the top
begin_snapshot_path = "snapshot_2024-09-09.json"
end_snapshot_path = "snapshot_2024-09-17.json"
csv_folder = "csvs"

# Ensure CSV folder exists
os.makedirs(csv_folder, exist_ok=True)

# Function to extract date from file name
def extract_date_from_filename(file_path):
    filename = os.path.basename(file_path)
    # Assuming the format snapshot_YYYY-MM-DD.json
    date_str = filename.split('_')[1].replace('.json', '')
    return datetime.strptime(date_str, '%Y-%m-%d')

# Function to load JSON file
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to save CSV file
def save_csv(data, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data[0].keys())  # Write header row based on the keys of the first dictionary
        for item in data:
            writer.writerow(item.values())  # Write rows of values

# Function to count tokens minted by each address and save CSV
def save_tokens_minted_by_address(data, output_file):
    # Count how many times each address appears in new_tokens
    token_count = Counter(entry['owner_addr'] for entry in data)
    
    # Write the results to a new CSV file
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['owner_addr', 'tokens_minted'])  # Header row
        for addr, count in token_count.items():
            writer.writerow([addr, count])  # Address and how many tokens they minted
    
    return token_count

# Function to print a report to the terminal
def print_report(begin_date, end_date, token_count, total_new_tokens):
    # Calculate days between snapshots
    days_between = (end_date - begin_date).days
    print("\n===== Minting Report =====")
    print(f"Begin Snapshot: {begin_date.strftime('%Y-%m-%d')}")
    print(f"End Snapshot: {end_date.strftime('%Y-%m-%d')}")
    print(f"Days Between: {days_between}")
    print(f"Total New Tokens Minted: {total_new_tokens}\n")
    print("Address, New Tokens Minted")
    
    # Sort addresses by tokens minted (biggest to smallest) and print
    for addr, count in sorted(token_count.items(), key=lambda x: x[1], reverse=True):
        print(f"{addr}, {count}")
    print("==========================\n")

# Load JSON data
begin_snapshot = load_json(begin_snapshot_path)
end_snapshot = load_json(end_snapshot_path)

# Extract dates from file names
begin_snapshot_date = extract_date_from_filename(begin_snapshot_path)
end_snapshot_date = extract_date_from_filename(end_snapshot_path)

# Save JSON data as CSV
save_csv(begin_snapshot, os.path.join(csv_folder, 'begin_snapshot.csv'))
save_csv(end_snapshot, os.path.join(csv_folder, 'end_snapshot.csv'))

# Create sets of token IDs for comparison
begin_token_ids = {entry['token_id'] for entry in begin_snapshot}
end_token_ids = {entry['token_id'] for entry in end_snapshot}

# Identify new tokens that exist in end_snapshot but not in begin_snapshot
new_token_ids = end_token_ids - begin_token_ids

# Extract entries with the new token IDs
new_tokens_data = [entry for entry in end_snapshot if entry['token_id'] in new_token_ids]

# Sort new tokens by token_id (assuming token_id is numeric)
sorted_new_tokens = sorted(new_tokens_data, key=lambda x: int(x['token_id']))

# Save new tokens in the same format as begin_snapshot and end_snapshot CSVs
save_csv(sorted_new_tokens, os.path.join(csv_folder, 'new_tokens.csv'))

# Save new addresses to CSV
new_addresses = {entry['owner_addr'] for entry in sorted_new_tokens}
with open(os.path.join(csv_folder, 'new_addresses.csv'), 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['owner_addr'])  # Header
    for addr in new_addresses:
        writer.writerow([addr])  # Write each new address

# Process new_tokens.csv to count tokens minted by each address
token_count = save_tokens_minted_by_address(sorted_new_tokens, os.path.join(csv_folder, 'tokens_minted_by_address.csv'))

# Print report to the terminal
total_new_tokens = len(new_tokens_data)
print_report(begin_snapshot_date, end_snapshot_date, token_count, total_new_tokens)

print(f"CSV files saved in {csv_folder}")