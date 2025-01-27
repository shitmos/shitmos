import json

# Define input and output file paths
input_file = "snapshot_2025-01-27.json"  # Replace with the path to your JSON file
output_file = "shitmos_wl.txt"

# Load the JSON data
with open(input_file, "r") as file:
    data = json.load(file)

# Extract all owner addresses
owner_addresses = [item["owner_addr"] for item in data]

# Write the owner addresses to a text file
with open(output_file, "w") as file:
    for address in owner_addresses:
        file.write(address + "\n")

print(f"Extracted {len(owner_addresses)} owner addresses to {output_file}.")
