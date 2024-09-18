import os
import json
import csv

# Input variables at the top
begin_snapshot_path = "snapshot_2024-09-09.json"
end_snapshot_path = "snapshot_2024-09-17.json"
csv_folder = "csvs"

# Ensure CSV folder exists
os.makedirs(csv_folder, exist_ok=True)

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

# Load JSON data
begin_snapshot = load_json(begin_snapshot_path)
end_snapshot = load_json(end_snapshot_path)

# Save JSON data as CSV
save_csv(begin_snapshot, os.path.join(csv_folder, 'begin_snapshot.csv'))
save_csv(end_snapshot, os.path.join(csv_folder, 'end_snapshot.csv'))

# Find new addresses in the end_snapshot
begin_addresses = {entry['owner_addr'] for entry in begin_snapshot}
end_addresses = {entry['owner_addr'] for entry in end_snapshot}
new_addresses = list(end_addresses - begin_addresses)

# Save new addresses to CSV
with open(os.path.join(csv_folder, 'new_addresses.csv'), 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['owner_addr'])  # Header
    for addr in new_addresses:
        writer.writerow([addr])  # Write each new address

print(f"CSV files saved in {csv_folder}")
