import json
import os
from collections import defaultdict

# Folder path where JSON files are stored
folder_path = "bibby_oe_trilogy/snapshots/2025-02-22"  # Adjust this to your actual folder path

# Store each file's data separately, indexed by filename
file_data = {}
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r") as file:
            data = json.load(file)
            # Collect owner counts
            file_data[filename] = defaultdict(int)
            for entry in data:
                owner_addr = entry["owner_addr"]
                file_data[filename][owner_addr] += 1  # Count tokens for each owner

# Track the output data
output_data = []
global_match_count = 1  # Initialize the global match counter

# Find all unique owner addresses across files
all_owner_addrs = set()
for data in file_data.values():
    all_owner_addrs.update(data.keys())

# Process each address to create entries in dump.json based on full sets
for owner_addr in all_owner_addrs:
    # Gather token counts for each file for the current address
    token_counts = [file_data[filename].get(owner_addr, 0) for filename in sorted(file_data.keys())]
    
    # Determine the number of full sets (minimum count across files)
    min_full_sets = min(token_counts)

    # Add an entry for each full set
    for _ in range(min_full_sets):
        output_data.append({
            "owner_addr": owner_addr,
            "dump_match_count": global_match_count,
        })
        global_match_count += 1  # Increment match count

# Write the output data to dump.json
output_file_path = "dump.json"
with open(output_file_path, "w") as output_file:
    json.dump(output_data, output_file, indent=4)

print(f"Data successfully written to {output_file_path}")
