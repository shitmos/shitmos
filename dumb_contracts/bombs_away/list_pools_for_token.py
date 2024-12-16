import os
import json

# Configuration: Set the token denom you're interested in
TOKEN_DENOM = "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/shitmos"  # Replace this with your desired denom
SNAPSHOT_DIR = "pool_snapshots"

def get_most_recent_snapshot(directory):
    files = [f for f in os.listdir(directory) if f.startswith("all_pools_") and f.endswith(".json")]
    if not files:
        print("No snapshot files found.")
        return None
    files.sort()  # Alphabetical sort; due to timestamp format YYYYMMDD_HHMMSS, last is the most recent
    return files[-1]

def load_pools(filename):
    path = os.path.join(SNAPSHOT_DIR, filename)
    with open(path, "r") as f:
        data = json.load(f)
    return data  # data should be a list of pool objects

def find_pools_with_token(pools, token_denom):
    matching_pools = []
    for pool in pools:
        pool_id = pool.get("id", "unknown")

        # Handle different possible fields
        if "pool_assets" in pool:
            pool_assets = pool["pool_assets"]
        elif "poolAssets" in pool:
            pool_assets = pool["poolAssets"]
        else:
            pool_assets = pool.get("pool_liquidity", [])

        # Check all assets in this array
        contains_token = False
        for asset in pool_assets:
            # `asset` might have a "token" subkey if it's `pool_assets`/`poolAssets`
            # If `pool_assets`, structure: [{"token": {"denom": "...", "amount": "..."}, "weight": ...}, ...]
            # If `pool_liquidity`, structure might be [{"denom":"...","amount":"..."}]
            token = asset.get("token", asset)
            denom = token.get("denom", "")
            if denom == token_denom:
                contains_token = True
                break  # We found the token in this pool, no need to check further assets

        if contains_token:
            matching_pools.append(pool_id)

    return matching_pools

def main():
    # Find the most recent snapshot file
    most_recent_file = get_most_recent_snapshot(SNAPSHOT_DIR)
    if not most_recent_file:
        return

    print(f"Using snapshot file: {most_recent_file}")

    # Load all pools from the snapshot
    pools = load_pools(most_recent_file)

    # Find all pools containing the specified token denom
    pools_with_token = find_pools_with_token(pools, TOKEN_DENOM)

    print(f"Pools containing '{TOKEN_DENOM}':")
    for pid in pools_with_token:
        print(pid)

if __name__ == "__main__":
    main()
