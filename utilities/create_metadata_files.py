import shutil
import os

def copy_json_files(original_file, start_num, end_num, file_location):
    base_name, extension = os.path.splitext(original_file)
    if extension.lower() != '.json':
        raise ValueError("The original file must be a JSON file.")

    original_path = os.path.join(file_location, original_file)

    for i in range(start_num, end_num + 1):
        new_file = f"{i}.json"
        new_file_path = os.path.join(file_location, new_file)
        shutil.copyfile(original_path, new_file_path)
        print(f"Copied {original_file} to {new_file}")

if __name__ == "__main__":
    # Config variables
    original_file = "1.json"  # Name of the original JSON file
    start_num = 2  # Beginning number for new JSON files
    end_num = 666  # Ending number for new JSON files
    file_location = "../nft/bibby-nft/shitpocalypse/metadata"  # Location of the JSON files

    # Ensure the directory exists
    os.makedirs(file_location, exist_ok=True)

    copy_json_files(original_file, start_num, end_num, file_location)
