import os
import json
import csv

# Path to the directory containing JSON metadata and the traits CSV file
directory_path = "../../../nft/nfts/metadata"
traits_file_path = "../data/traits.csv"

# Function to read the latest trait type and trait value from the traits CSV file
def get_latest_trait(file_path):
    max_order = 0
    latest_trait_info = None
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            order = int(row['order'])
            if order > max_order:
                max_order = order
                latest_trait_info = (row['trait_type'], row['value'])
    return latest_trait_info

# Function to identify token IDs with specific trait type and value
def identify_trait_specific_ids(directory, traits_file):
    trait_data = get_latest_trait(traits_file)
    if trait_data is None:
        print("No valid trait data found.")
        return []

    trait_type, trait_value = trait_data
    matching_ids = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                for trait in data.get("attributes", []):
                    if trait.get("trait_type") == trait_type and trait.get("value") == trait_value:
                        matching_ids.append(filename.replace('.json', ''))
                        break
    return matching_ids

# Get list of token IDs that match the latest trait type and value
matching_token_ids = identify_trait_specific_ids(directory_path, traits_file_path)
if matching_token_ids:
    print("Matching Token IDs:", matching_token_ids)
    print("Total Matching IDs:", len(matching_token_ids))
else:
    print("No matching tokens found.")
