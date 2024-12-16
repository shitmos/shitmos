import os
import json
import subprocess
import datetime
import time

# Configuration
TOKEN_DENOM = "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/shitmos"  # The token denom you're interested in
TOKEN_NAME = "shitmos"  # A human-readable name for the token
NODE_URL = "https://rpc.osmosis.zone"
SNAPSHOT_DIR = "pool_snapshots"
PAGE_LIMIT = 10000  # number of owners to fetch in one go

def get_most_recent_all_pools_file(directory):
    files = [f for f in os.listdir(directory) if f.startswith("all_pools_") and f.endswith(".json")]
    if not files:
        print("No all_pools files found in", directory)
        return None
    files.sort()
    return files[-1]

def load_pools(filename):
    path = os.path.join(SNAPSHOT_DIR, filename)
    with open(path, "r") as f:
        data = json.load(f)
    return data

def find_pools_with_token(pools, token_denom):
    matching_pools = []
    for pool in pools:
        pool_id = pool.get("id", "unknown")

        # Identify which field has the assets
        if "pool_assets" in pool:
            pool_assets = pool["pool_assets"]
        elif "poolAssets" in pool:
            pool_assets = pool["poolAssets"]
        else:
            pool_assets = pool.get("pool_liquidity", [])

        contains_token = False
        for asset in pool_assets:
            token = asset.get("token", asset)
            denom = token.get("denom", "")
            if denom == token_denom:
                contains_token = True
                break
        if contains_token:
            matching_pools.append(pool_id)
    return matching_pools

def fetch_pool_owners(denom):
    # Replicate the working command:
    # osmosisd q bank denom-owners gamm/pool/<pool_id> --node <NODE_URL> --page-limit 10000 -o json 2>&1
    cmd = [
        "osmosisd", "q", "bank", "denom-owners",
        denom,
        "--node", NODE_URL,
        "--page-limit", str(PAGE_LIMIT),
        "-o", "json"
    ]

    # Merge stderr into stdout so we get identical output as terminal with 2>&1
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    if result.returncode != 0:
        print(f"Error fetching owners for {denom}:\n{result.stdout}")
        return []

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Invalid JSON output when fetching owners for {denom}.")
        print("Combined output:")
        print(result.stdout)
        return []

    denom_owners = data.get("denom_owners", [])
    return denom_owners

def main():
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)

    # Get the most recent all_pools file
    all_pools_file = get_most_recent_all_pools_file(SNAPSHOT_DIR)
    if not all_pools_file:
        return

    print(f"Using all pools file: {all_pools_file}")
    pools = load_pools(all_pools_file)

    # Find pools containing TOKEN_DENOM
    pools_with_token = find_pools_with_token(pools, TOKEN_DENOM)
    print(f"Found {len(pools_with_token)} pools containing {TOKEN_DENOM}")

    # Create a timestamp for naming files
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Write pools_for_<TOKEN_NAME>_<timestamp>.json
    pools_for_token_file = os.path.join(SNAPSHOT_DIR, f"pools_for_{TOKEN_NAME}_{timestamp}.json")
    with open(pools_for_token_file, "w") as f:
        json.dump(pools_with_token, f, indent=2)
    print(f"Pools for {TOKEN_NAME} saved to {pools_for_token_file}")

    # Track number of LPers for summary
    pool_owners_count = {}

    # For each pool, run the denom-owners command
    for pool_id in pools_with_token:
        denom = f"gamm/pool/{pool_id}"
        print(f"Fetching LP owners for pool {pool_id} (denom={denom})...")
        owners = fetch_pool_owners(denom)

        # Save LP owners to a timestamped file
        lp_filename = os.path.join(SNAPSHOT_DIR, f"lp_addresses_for_{TOKEN_NAME}_{pool_id}_{timestamp}.json")
        with open(lp_filename, "w") as f:
            json.dump(owners, f, indent=2)
        print(f"LP owners for pool {pool_id} saved to {lp_filename}")

        pool_owners_count[pool_id] = len(owners)

        # Optional delay
        time.sleep(0.2)

    # Print out summary
    print(f"\nThere are {len(pools_with_token)} pools with {TOKEN_NAME}")
    for pid, count in pool_owners_count.items():
        print(f"pool {pid} has {count} liquidity providers")

if __name__ == "__main__":
    main()