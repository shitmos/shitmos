import csv
from bech32 import bech32_decode, bech32_encode

# Function to convert Stargaze address to Osmosis address
def convert_address_to_osmosis(stars_address):
    hrp, data = bech32_decode(stars_address)
    if hrp == "stars":
        return bech32_encode("osmo", data)
    return stars_address  # Return the original address if the prefix doesn't match

# Input and output file paths
input_file = "nice_list.csv"  # Replace with the path to your input CSV file
output_file = "nice_list_osmo.csv"  # Replace with the path for the output CSV file

# Read the input CSV and convert addresses
with open(input_file, mode="r", newline="") as infile:
    reader = csv.reader(infile)
    rows = [row for row in reader]

# Update the Stargaze addresses to Osmosis addresses
for row in rows[1:]:  # Skip header row
    row[0] = convert_address_to_osmosis(row[0])  # Convert the first column

# Write the updated data to the output CSV
with open(output_file, mode="w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(rows)

print(f"Converted CSV has been saved to {output_file}")
