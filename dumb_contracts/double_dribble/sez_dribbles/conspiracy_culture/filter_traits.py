import json
import os

# Configuration section
SNAPSHOT_FILE = "snapshots/snapshot_2024-11-15.json"
METADATA_FOLDER = "metadata"
OUTPUT_FOLDER = "snapshots"  # Folder to save output files

TRAIT_FILTERS = {
    "Head Gear": "Foil Wizard"
}

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

# Function to check if metadata matches any single filter
def matches_single_filter(metadata, trait_type, trait_value):
    if not metadata or "attributes" not in metadata:
        return False
    for attribute in metadata["attributes"]:
        if attribute.get("trait_type") == trait_type and attribute.get("value") == trait_value:
            return True
    return False

# Function to check if metadata matches all filters
def matches_all_filters(metadata, filters):
    if not metadata or "attributes" not in metadata:
        return False
    matched_traits = 0
    for attribute in metadata["attributes"]:
        trait_type = attribute.get("trait_type")
        value = attribute.get("value")
        if trait_type in filters and filters[trait_type] == value:
            matched_traits += 1
    return matched_traits == len(filters)

# Function to check how many filters an NFT matches
def count_matching_filters(metadata, filters):
    if not metadata or "attributes" not in metadata:
        return 0
    matched_traits = 0
    for attribute in metadata["attributes"]:
        trait_type = attribute.get("trait_type")
        value = attribute.get("value")
        if trait_type in filters and filters[trait_type] == value:
            matched_traits += 1
    return matched_traits

# Function to filter and categorize snapshot data
def filter_snapshot(snapshot_data, filters):
    individual_filtered = {key: [] for key in filters}
    all_filtered = []
    overlap_filtered = {i: [] for i in range(2, len(filters))}  # Overlap for 2 or more traits

    for record in snapshot_data:
        token_id = record["token_id"]
        metadata = load_metadata(token_id)

        # Check individual trait matches
        for trait_type, trait_value in filters.items():
            if matches_single_filter(metadata, trait_type, trait_value):
                individual_filtered[trait_type].append(record)

        # Check if all traits match
        if matches_all_filters(metadata, filters):
            all_filtered.append(record)

        # Check for overlaps (multiple matches but not all)
        match_count = count_matching_filters(metadata, filters)
        if 1 < match_count < len(filters):
            overlap_filtered[match_count].append(record)

    return individual_filtered, all_filtered, overlap_filtered

# Save JSON data to a file
def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    snapshot_data = load_snapshot(SNAPSHOT_FILE)
    individual_filtered, all_filtered, overlap_filtered = filter_snapshot(snapshot_data, TRAIT_FILTERS)

    # Save individual trait filter results
    for trait_type in TRAIT_FILTERS:
        filename = os.path.join(OUTPUT_FOLDER, f"filtered_{trait_type}.json")
        save_json(individual_filtered[trait_type], filename)
        print(f"Saved filtered NFTs for {trait_type} to {filename}")
        print(f"{trait_type}: {len(individual_filtered[trait_type])} matches")

    # Save all traits match results
    all_filename = os.path.join(OUTPUT_FOLDER, "filtered_all_traits.json")
    save_json(all_filtered, all_filename)
    print(f"Saved filtered NFTs that match all traits to {all_filename}")
    print(f"All Traits: {len(all_filtered)} matches")

    # Save overlap matches (multiple but not all traits)
    for match_count in overlap_filtered:
        filename = os.path.join(OUTPUT_FOLDER, f"filtered_{match_count}_trait_overlap.json")
        save_json(overlap_filtered[match_count], filename)
        print(f"Saved filtered NFTs with {match_count} trait overlaps to {filename}")
        print(f"Overlap of {match_count} traits: {len(overlap_filtered[match_count])} matches")
