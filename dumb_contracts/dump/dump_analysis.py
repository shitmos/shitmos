import json
import os
from collections import defaultdict

# Folder path where the JSON snapshot files are stored
folder_path = "snapshots/2024-10-31"  # Replace this with your folder path

# Load dump.json to analyze full matches
with open("dump.json", "r") as file:
    dump_data = json.load(file)

# Dictionary to count occurrences of each address in dump.json (for full matches)
address_full_match_counts = defaultdict(int)

# Count each occurrence of owner_addr in dump.json
for entry in dump_data:
    owner_addr = entry["owner_addr"]
    address_full_match_counts[owner_addr] += 1

# Get the maximum number of matches for any address
max_full_matches = max(address_full_match_counts.values()) if address_full_match_counts else 0

# Summary of addresses by full match count
print("Full Matches:")
for i in range(1, max_full_matches + 1):
    count = sum(1 for addr in address_full_match_counts if address_full_match_counts[addr] == i)
    print(f"addresses with {i} match{'es' if i > 1 else ''}: {count}")

print("\n---\n")  # Divider between full matches and partial matches analysis

# Load all snapshot files to analyze partial matches
snapshot_data = {}  # Dictionary to store data from each snapshot file by filename
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r") as file:
            data = json.load(file)
            snapshot_data[filename] = data  # Store entire file data by filename

# Dictionary to track addresses and their token counts in each snapshot file
partial_match_counts = defaultdict(lambda: defaultdict(int))

# Count tokens for each address in each file
for filename, entries in snapshot_data.items():
    for entry in entries:
        owner_addr = entry["owner_addr"]
        partial_match_counts[owner_addr][filename] += 1  # Increment count for each token

# Identify and print addresses with partial matches (appears in at least 2 files)
print("Partial Matches (appears in at least 2 files):")
for owner_addr, file_counts in partial_match_counts.items():
    # Check if this is a partial match (appears in at least 2 files but not all files)
    if 1 < len(file_counts) < len(snapshot_data):  # At least 2 files but not all
        print(f"Wallet: {owner_addr}")
        for filename in sorted(snapshot_data.keys()):
            print(f"{filename} -> {file_counts.get(filename, 0)}")  # Print token count per file
        print()  # Blank line between partial matches
