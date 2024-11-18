import json
import os

# Configuration section
SNAPSHOT_FILE = "snapshots/2024-11-18/conspiracy2_snapshot_2024-11-18.json"  # Update with your snapshot file path
OUTPUT_FILE = "conspiracy2_2024-11-18.txt"  # Output file to save the list of addresses

# Function to load the snapshot data
def load_snapshot(snapshot_file):
    with open(snapshot_file, 'r') as f:
        return json.load(f)

# Function to extract addresses from the snapshot
def extract_addresses(snapshot_data):
    addresses = []
    for record in snapshot_data:
        addresses.append(record["owner_addr"])
    return addresses

# Function to save the addresses to a text file
def save_addresses_to_file(addresses, output_file):
    with open(output_file, 'w') as f:
        for address in addresses:
            f.write(f"{address}\n")

if __name__ == "__main__":
    # Load the snapshot data
    snapshot_data = load_snapshot(SNAPSHOT_FILE)
    
    # Extract addresses from the snapshot
    addresses = extract_addresses(snapshot_data)
    
    # Save the addresses to a text file
    save_addresses_to_file(addresses, OUTPUT_FILE)
    
    print(f"Address list saved to {OUTPUT_FILE}")
