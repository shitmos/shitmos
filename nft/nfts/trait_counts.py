import os
import json
from collections import defaultdict

# Configuration
METADATA_DIR = 'metadata'  # Folder containing the JSON files
OUTPUT_FILE = 'trait_counts.json'  # Output file for trait counts

def collect_traits(metadata_dir):
    trait_counts = defaultdict(lambda: defaultdict(int))

    for filename in os.listdir(metadata_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(metadata_dir, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                for attribute in data.get('attributes', []):
                    trait_type = attribute['trait_type']
                    trait_value = attribute['value']
                    trait_counts[trait_type][trait_value] += 1

    return trait_counts

def save_traits_to_file(trait_counts, output_file):
    with open(output_file, 'w') as file:
        json.dump(trait_counts, file, indent=4)

if __name__ == "__main__":
    trait_counts = collect_traits(METADATA_DIR)
    save_traits_to_file(trait_counts, OUTPUT_FILE)

    print(f"Trait counts saved to {OUTPUT_FILE}")
