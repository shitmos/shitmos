import os
import random
import json

# Directory containing JSON metadata files
metadata_dir = "metadata"
shuffled_metadata_dir = "shuffled_metadata"

# Ensure the shuffled directory exists
os.makedirs(shuffled_metadata_dir, exist_ok=True)

def shuffle_metadata_ids(metadata_dir, shuffled_metadata_dir):
    # Get all JSON files in the directory
    json_files = [f for f in os.listdir(metadata_dir) if f.endswith(".json")]

    # Parse the current IDs and shuffle them
    ids = [int(os.path.splitext(f)[0]) for f in json_files]
    random.shuffle(ids)

    # Create a mapping of old IDs to new shuffled IDs
    mapping = {old: new for old, new in zip(sorted(ids), ids)}

    # Copy files to the shuffled directory with new shuffled IDs
    for old_id, new_id in mapping.items():
        old_path = os.path.join(metadata_dir, f"{old_id}.json")
        new_path = os.path.join(shuffled_metadata_dir, f"{new_id}.json")
        with open(old_path, "r") as old_file:
            data = json.load(old_file)
        with open(new_path, "w") as new_file:
            json.dump(data, new_file, indent=4)
        print(f"{old_id}.json shuffled to {new_id}.json")

    print("Metadata IDs shuffled successfully! Files saved in 'shuffled_metadata' directory.")

# Run the function
shuffle_metadata_ids(metadata_dir, shuffled_metadata_dir)
