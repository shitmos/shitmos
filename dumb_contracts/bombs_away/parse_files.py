import os
import json
import csv
from datetime import datetime

# Input folder containing the JSON files
INPUT_FOLDER = "jsons"

# Output CSV file name
current_date = datetime.now().strftime("%Y-%m-%d")
output_file = f"lpers_{current_date}.csv"

# Function to parse JSON files and write to CSV
def parse_json_to_csv(input_folder, output_csv):
    json_files = [f for f in os.listdir(input_folder) if f.endswith(".json")]

    print("Found JSON files:")
    for json_file in json_files:
        print(f"- {json_file}")

    with open(output_csv, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Address", "Pool", "Amount"])  # Write header

        # Process each JSON file
        for json_file in json_files:
            file_path = os.path.join(input_folder, json_file)
            with open(file_path, "r") as f:
                data = json.load(f)
                for entry in data:
                    address = entry.get("address", "")
                    pool = entry["balance"].get("denom", "").split("/")[-1]  # Extract pool ID
                    amount = entry["balance"].get("amount", "")
                    csv_writer.writerow([address, pool, amount])

    print(f"CSV file created: {output_csv}")

# Run the script
if __name__ == "__main__":
    parse_json_to_csv(INPUT_FOLDER, output_file)