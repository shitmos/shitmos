import subprocess
import json
import datetime
import os

# Configuration
NODE_URL = "https://rpc.osmosis.zone"
SNAPSHOT_DIR = "pool_snapshots"

def print_distinct_types(all_pools):
    distinct_types = set()
    for pool in all_pools:
        t = pool.get("@type", None)
        if t:
            distinct_types.add(t)
    if distinct_types:
        print("\nDistinct @type values found:")
        for t in distinct_types:
            print(t)
    else:
        print("\nNo @type fields found in the pools.")


def main():
    # Ensure the snapshot directory exists
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)

    # Run the command to get all pools as JSON
    cmd = [
        "osmosisd", "query", "poolmanager", "all-pools",
        "--node", NODE_URL,
        "-o", "json"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error fetching pools:", result.stderr)
        return

    # Parse the JSON output
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print("Invalid JSON output from the command.")
        print("stdout:", result.stdout)
        print("stderr:", result.stderr)
        return

    # Extract the pools array
    all_pools = data.get("pools", [])
    print(f"Retrieved {len(all_pools)} pools.")

    # Generate a timestamped filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(SNAPSHOT_DIR, f"all_pools_{timestamp}.json")

    # Save the combined result
    with open(filename, "w") as f:
        json.dump(all_pools, f, indent=2)

    print(f"All {len(all_pools)} pools saved to {filename}")

    # Print distinct @type values
    print_distinct_types(all_pools)

if __name__ == "__main__":
    main()
