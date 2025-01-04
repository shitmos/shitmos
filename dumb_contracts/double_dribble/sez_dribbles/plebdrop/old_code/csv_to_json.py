import csv
import json
import os

def generate_json_from_csv(input_csv, output_json):
    """
    Read a CSV file containing addresses and generate a JSON file with the specified structure.

    Args:
        input_csv (str): Path to the input CSV file.
        output_json (str): Path to the output JSON file.
    """
    # Ensure the input CSV exists
    if not os.path.exists(input_csv):
        print(f"Error: Input CSV file '{input_csv}' does not exist.")
        return

    # Read the CSV and construct the JSON structure
    result = []
    try:
        with open(input_csv, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            # Check if the required column exists
            if 'address' not in reader.fieldnames:
                print("Error: The CSV file must have a column named 'address'.")
                return

            for row in reader:
                entry = {
                    "address": row['address'],
                    "token_id": "1",
                    "is_listed": False,
                    "is_in_pool": False,
                    "is_staked": False,
                    "dao_address": None
                }
                result.append(entry)

    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # Write the JSON structure to the output file
    try:
        with open(output_json, 'w', encoding='utf-8') as jsonfile:
            json.dump(result, jsonfile, indent=2)
        print(f"JSON file successfully written to '{output_json}'.")
    except Exception as e:
        print(f"Error writing JSON file: {e}")

if __name__ == "__main__":
    # Replace with your input CSV file and output JSON file paths
    input_csv_path = "snapshots/naughty_list.csv"  # Update this to the path of your input CSV
    output_json_path = "snapshot.json"  # Update this to your desired output JSON file path

    generate_json_from_csv(input_csv_path, output_json_path)
