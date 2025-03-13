import csv
import json
import os

def convert_csv_to_json(csv_file_path, json_file_path):
    data = []
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            record = {
                "owner_addr": row["address"],
                "token_id": row["tokenId"],
                "is_listed": None,
                "is_in_pool": None,
                "is_staked": None,
                "dao_address": None
            }
            data.append(record)
    with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=2)

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            csv_path = os.path.join(folder_path, filename)
            json_filename = filename.rsplit('.', 1)[0] + '.json'
            json_path = os.path.join(folder_path, json_filename)
            convert_csv_to_json(csv_path, json_path)
            print(f'Converted {csv_path} to {json_path}')

if __name__ == "__main__":
    # Replace 'path/to/your/csv/folder' with the actual folder path containing your CSV files
    folder_path = 'bibby_oe_trilogy/snapshots/2025-02-22'
    process_folder(folder_path)
