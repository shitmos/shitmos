import json
import os
import bech32

# Define the directory paths
DATA_DIR = '/data'
COLLECTIONS_FILE = os.path.join(DATA_DIR, 'collections.json')
OUTPUT_FILE = os.path.join(DATA_DIR, 'converted_addresses.json')

# Load collection data from JSON file
with open(COLLECTIONS_FILE, 'r') as file:
    collections_data = json.load(file)

def convert_address(stargaze_address, target_prefix="osmo"):
    """
    Convert a Stargaze address to an Osmosis address.
    """
    hrp, data = bech32.bech32_decode(stargaze_address)
    osmosis_address = bech32.bech32_encode(target_prefix, data)
    return osmosis_address

def convert_and_save_addresses(collections):
    converted_data = {"recipients": []}
    
    for collection in collections:
        recipients = collection['recipients']
        
        for recipient in recipients:
            stargaze_address = recipient['address']
            osmosis_address = convert_address(stargaze_address)
            converted_data["recipients"].append({
                "name": recipient['label'],
                "stargaze_address": stargaze_address,
                "osmosis_address": osmosis_address
            })

    # Save the converted addresses to a JSON file
    with open(OUTPUT_FILE, 'w') as outfile:
        json.dump(converted_data, outfile, indent=4)

def main():
    collections = collections_data['collections']
    convert_and_save_addresses(collections)
    print(f"Converted addresses saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
