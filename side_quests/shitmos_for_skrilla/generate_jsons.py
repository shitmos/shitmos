import csv
import json
import os

# Input CSV file and output directory
csv_file = "metadata.csv"
output_dir = "metadata"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

def generate_json_from_csv(csv_file, output_dir):
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Construct the JSON structure
            nft_data = {
                "name": row["name"],
                "description": row["description"],
                "attributes": [
                    {"trait_type": "Character", "value": row["Character"]},
                    {"trait_type": "Special", "value": row["Special"]}
                ],
                "image": row["image"]
            }

            # Output file path
            output_file = os.path.join(output_dir, f"{row['token id']}.json")

            # Write JSON to file
            with open(output_file, "w") as json_file:
                json.dump(nft_data, json_file, indent=4)

    print(f"Generated JSON files in {output_dir}")

# Run the function
generate_json_from_csv(csv_file, output_dir)
