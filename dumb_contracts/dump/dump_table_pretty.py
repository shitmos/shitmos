import json
import os
from collections import defaultdict

# Folder path where the JSON snapshot files are stored
folder_path = "bibby_oe_trilogy/snapshots/2025-02-22"  # Replace this with your folder path

# Load dump.json to analyze full matches
with open("dump.json", "r") as file:
    dump_data = json.load(file)

# Load collections.txt to get names and addresses
collections = []
with open("bibby_oe_trilogy/collections.txt", "r") as file:
    next(file)  # Skip the header row
    for line in file:
        name, address = line.strip().split(", ")
        collections.append((name, address))

# Set a maximum width for each collection column based on the longest single word in the names
max_column_width = max(len(word) for name, _ in collections for word in name.split())

# Calculate the maximum width for the address column based on the longest address
address_column_width = max(len(entry["owner_addr"]) for entry in dump_data)

# Function to wrap and bottom-align text for headers
def wrap_text_bottom_justify(text, width, max_lines):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        if len(line) + len(word) + 1 <= width:
            line += word + " "
        else:
            lines.append(line.strip())
            line = word + " "
    lines.append(line.strip())

    # Bottom-justify by adding empty lines at the top, then center each line within the width
    while len(lines) < max_lines:
        lines.insert(0, "")

    return [line.center(width) for line in lines]

# Wrap each collection name to fit within the max column width and calculate max lines for headers
wrapped_headers = [wrap_text_bottom_justify(name, max_column_width, max_lines=3) for name, _ in collections]
max_lines = max(len(header) for header in wrapped_headers)  # Find the tallest header

# Adjust all headers to have the same number of lines
adjusted_header_rows = [[" " * address_column_width] * (max_lines - 1) + ["Address".ljust(address_column_width)]]
for i in range(max_lines):
    header_line = [
        wrapped_headers[j][i] if i < len(wrapped_headers[j]) else " " * max_column_width
        for j in range(len(wrapped_headers))
    ]
    adjusted_header_rows.append(header_line)

adjusted_header_rows[-1].append("Dump Count".center(max_column_width))  # Add "Dump Count" only in the last line

# Dictionary to count occurrences of each address for dump_count
address_full_match_counts = defaultdict(int)

# Count each occurrence of owner_addr in dump.json
for entry in dump_data:
    owner_addr = entry["owner_addr"]
    address_full_match_counts[owner_addr] += 1

# Load all snapshot files to analyze partial matches
snapshot_data = {}  # Dictionary to store data from each snapshot file by filename
file_names = []
for idx, filename in enumerate(os.listdir(folder_path)):
    if filename.endswith(".json"):
        file_names.append(filename)
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r") as file:
            data = json.load(file)
            snapshot_data[filename] = data  # Store entire file data by filename

# Dictionary to track addresses and their token counts in each snapshot file
address_token_counts = defaultdict(lambda: defaultdict(int))

# Count tokens for each address in each file
for idx, filename in enumerate(sorted(snapshot_data.keys())):
    for entry in snapshot_data[filename]:
        owner_addr = entry["owner_addr"]
        address_token_counts[owner_addr][collections[idx][0]] += 1  # Increment count for each token

# Create a table of addresses, counts in each file, and dump_count
table_data = []
for owner_addr, file_counts in address_token_counts.items():
    # Get token counts for each file
    counts_per_file = [file_counts.get(name, 0) for name, _ in collections[:len(file_names)]]
    # Determine if it's a full match by checking if the owner appears in all files
    is_full_match = len(file_counts) == len(snapshot_data)
    # Calculate dump_count as min of counts_per_file if it's a full match, else 0
    dump_count = min(counts_per_file) if is_full_match else 0
    # Only add rows with dump_count >= 1
    if dump_count >= 1:
        table_data.append([owner_addr] + counts_per_file + [dump_count])

# Sort table: dump_count (descending), then by each file count (descending)
table_data.sort(key=lambda row: (row[-1], *row[1:-1]), reverse=True)

# Calculate totals for each column
totals = ["Total"] + [sum(row[i] for row in table_data) for i in range(1, len(collections) + 2)]

# Calculate divider width based on the entire header row
divider_length = (address_column_width + (max_column_width * (len(collections) + 1))) + (3 * (len(collections) + 1))

# Write to text file with aligned columns
output_file_path = "dump_table_output.txt"
with open(output_file_path, "w") as file:
    # Print each line of headers, with "Address" appearing only once at the bottom of the header section
    for i in range(max_lines):
        if i == max_lines - 1:  # Last line with "Dump Count" at the end
            file.write(f"{'Address'.ljust(address_column_width)}   " + "   ".join(f"{text:<{max_column_width}}" for text in adjusted_header_rows[i]) + f"   {'Dump Count':<{max_column_width}}\n")
        else:
            file.write(" " * address_column_width + "   " + "   ".join(f"{text:<{max_column_width}}" for text in adjusted_header_rows[i]) + "\n")

    file.write("-" * divider_length + "\n")

    # Print each row with aligned columns
    for row in table_data:
        # Center-align each data entry within the column width
        file.write(f"{row[0]:<{address_column_width}}   " + "   ".join(f"{str(row[i]).center(max_column_width)}" for i in range(1, len(row))) + "\n")

    # Print totals row at the bottom
    file.write("-" * divider_length + "\n")  # Divider line before totals
    file.write("   ".join(f"{totals[i]:<{max_column_width if i > 0 else address_column_width}}" for i in range(len(totals))) + "\n")

print(f"Data successfully written to {output_file_path}")
