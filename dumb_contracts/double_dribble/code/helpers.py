import os
import glob
from datetime import datetime

def get_latest_snapshot_file(directory):
    # Create the pattern for matching snapshot files
    pattern = os.path.join(directory, "snapshot_*.csv")
    
    # Use glob to find all files matching the pattern
    snapshot_files = glob.glob(pattern)
    # Filter out files that do not match the expected date format
    valid_snapshot_files = []
    for file in snapshot_files:
        try:
            datetime.strptime(os.path.basename(file), "snapshot_%Y-%m-%d.csv")
            valid_snapshot_files.append(file)
        except ValueError:
            pass

    if not valid_snapshot_files:
        print("No valid snapshot files matched the pattern.")
        return None
    
    # Sort the valid files by date suffix in descending order
    valid_snapshot_files.sort(reverse=True, key=lambda x: datetime.strptime(os.path.basename(x), "snapshot_%Y-%m-%d.csv"))
    
    # Return the latest snapshot file
    return valid_snapshot_files[0] if valid_snapshot_files else None
