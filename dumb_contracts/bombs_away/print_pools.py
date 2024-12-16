import subprocess
import json
import time
import datetime
import os

NODE_URL = "https://rpc.osmosis.zone"
LIMIT = 100  # Number of pools to fetch per page
SNAPSHOT_DIR = "pool_snapshots"  # Directory to store snapshots

def get_total_pools():
    cmd = ["osmosisd", "q", "gamm", "num-pools", "--node", NODE_URL, "-o", "json"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error fetching total pools:", result.stderr)
        exit(1)
    data = json.loads(result.stdout)
    return int(data.get("num_pools", 0))

def fetch_pools_in_pages(total_pools):
    pages = (total_pools + LIMIT - 1) // LIMIT
    all_pools = []
    for i in range(1, pages + 1):
        print(f"Fetching page {i} of {pages} (limit={LIMIT})...")
        cmd = [
            "osmosisd", "query", "poolmanager", "all-pools",
            "--node", NODE_URL,
            "--page", str(i),
            "--limit", str(LIMIT),
            "-o", "json"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error fetching page {i}:", result.stderr)
            continue

        data = json.loads(result.stdout)
        page_pools = data.get("pools", [])
        all_pools.extend(page_pools)

        # Small delay to be polite to the node
        time.sleep(0.2)

    return all_pools

def main():
    total_pools = get_total_pools()
    print(f"Total pools: {total_pools}")

    all_pools = fetch_pools_in_pages(total_pools)

    # Ensure the snapshot directory exists
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)

    # Generate a timestamped filename inside the pool_snapshots directory
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(SNAPSHOT_DIR, f"all_pools_{timestamp}.json")

    # Save the combined result
    with open(filename, "w") as f:
        json.dump(all_pools, f, indent=2)

    print(f"All {len(all_pools)} pools saved to {filename}")

if __name__ == "__main__":
    main()
