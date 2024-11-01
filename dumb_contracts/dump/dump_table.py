import json
import os
from collections import defaultdict

# Folder path where the JSON snapshot files are stored
folder_path = "snapshots/2024-10-31"  # Replace this with your folder path

# Load dump.json to analyze full matches
with open(os.path.join(folder_path, "dump.json"), "r") as file:
    dump_data = json.load(file)

# Dictionary to count occurrences of each address in dump.json (for full matches)
address_full_match_counts = defaultdict(int)

# Count each occurrence of owner_addr in dump.json
for entry in dump_data:
    owner_addr = entry["owner_addr"]
    address_full_match_counts[owner_addr] += 1

# Load all snapshot files (excluding dump.json) to analyze partial matches
snapshot_data = {}  # Dictionary to store data from each snapshot file by filename
file_names = []
for filename in os.listdir(folder_path):
    if filename.endswith(".json") and filename != "dump.json":
        file_names.append(filename)
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r") as file:
            data = json.load(file)
            snapshot_data[filename] = data  # Store entire file data by filename

# Dictionary to track addresses and their token counts in each snapshot file
address_token_counts = defaultdict(lambda: defaultdict(int))

# Count tokens for each address in each file
for filename, entries in snapshot_data.items():
    for entry in entries:
        owner_addr = entry["owner_addr"]
        address_token_counts[owner_addr][filename] += 1  # Increment count for each token

# Create a table of addresses, counts in each file, and dump_count
table_data = []
for owner_addr, file_counts in address_token_counts.items():
    # Get token counts for each file
    counts_per_file = [file_counts.get(filename, 0) for filename in sorted(snapshot_data.keys())]
    # Determine if it's a full match by checking if the owner appears in all files
    is_full_match = len(file_counts) == len(snapshot_data)
    # Calculate dump_count as min of counts_per_file if it's a full match, else 0
    dump_count = min(counts_per_file) if is_full_match else 0
    # Append row to the table data
    table_data.append([owner_addr] + counts_per_file + [dump_count])

# Sort table: dump_count (descending), then by each file count (descending)
table_data.sort(key=lambda row: (row[-1], *row[1:-1]), reverse=True)

# Print header (excluding dump.json)
header = ["address"] + sorted(snapshot_data.keys()) + ["dump_count"]
print(", ".join(header))

# Print table rows
for row in table_data:
    print(", ".join(map(str, row)))
