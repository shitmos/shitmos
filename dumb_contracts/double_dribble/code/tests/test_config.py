# test_config.py

import sys
import os

# Add the parent directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config

def main():
    # Print the SNAPSHOT_FILE to verify it is correctly identified
    print(f"Latest snapshot file: {config.SNAPSHOT_FILE}")

if __name__ == "__main__":
    main()
