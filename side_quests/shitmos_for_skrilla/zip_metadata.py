import os
import random
import json
import zipfile

# Directory containing JSON metadata files
metadata_dir = "metadata"
shuffled_metadata_dir = "shuffled_metadata"
zip_file_name = "shuffled_metadata.zip"

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

def zip_shuffled_metadata(shuffled_metadata_dir, zip_file_name):
    # Create a ZIP file of the shuffled metadata directory
    with zipfile.ZipFile(zip_file_name, "w") as zipf:
        for root, _, files in os.walk(shuffled_metadata_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, shuffled_metadata_dir)
                zipf.write(file_path, arcname)
    print(f"Shuffled metadata directory zipped into {zip_file_name}")

# Run the functions
shuffle_metadata_ids(metadata_dir, shuffled_metadata_dir)
zip_shuffled_metadata(shuffled_metadata_dir, zip_file_name)
