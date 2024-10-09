import json
import os

# Configuration section
SNAPSHOT_FILE = "snapshots/snapshot_2024-10-01.json"  # Update with your snapshot file path
METADATA_FOLDER = "metadata"  # Update with your metadata folder path

# Define the trait_type and value you want to filter by
TRAIT_TYPE = "Misc"
TRAIT_VALUE = "Bee Kind"

# Function to load snapshot data
def load_snapshot(snapshot_file):
    with open(snapshot_file, 'r') as f:
        return json.load(f)

# Function to load metadata for a given token ID
def load_metadata(token_id):
    metadata_file = os.path.join(METADATA_FOLDER, f"{token_id}.json")
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            return json.load(f)
    return None

# Function to check if the metadata contains the trait_type and value
def has_trait(metadata, trait_type, trait_value):
    if not metadata or "attributes" not in metadata:
        return False
    for attribute in metadata["attributes"]:
        if attribute.get("trait_type") == trait_type and attribute.get("value") == trait_value:
            return True
    return False

# Main function to print token IDs that match the trait filter
def print_matching_ids(snapshot_data, trait_type, trait_value):
    matching_ids = []
    for record in snapshot_data:
        token_id = record["token_id"]
        metadata = load_metadata(token_id)
        if has_trait(metadata, trait_type, trait_value):
            matching_ids.append(token_id)
    return matching_ids

if __name__ == "__main__":
    snapshot_data = load_snapshot(SNAPSHOT_FILE)
    matching_ids = print_matching_ids(snapshot_data, TRAIT_TYPE, TRAIT_VALUE)

    print(f"Token IDs that match {TRAIT_TYPE}: {TRAIT_VALUE}")
    for token_id in matching_ids:
        print(token_id)
