import os
import json
import base64
import subprocess
import datetime
import time

# Configuration
TOKEN_DENOM = "factory/osmo1n6asrjy9754q8y9jsxqf557zmsv3s3xa5m9eg5/uspice"  # The token denom you're interested in
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
    return data  # should be a list of pool objects

def pool_contains_token(pool, token_denom):
    pool_type = pool.get("@type", "")

    if pool_type == "/osmosis.gamm.v1beta1.Pool":
        # Vanilla GAMM pool: "pool_assets"
        pool_assets = pool.get("pool_assets", [])
        for asset in pool_assets:
            token = asset.get("token", {})
            denom = token.get("denom", "")
            if denom == token_denom:
                return True

    elif pool_type == "/osmosis.gamm.poolmodels.stableswap.v1beta1.Pool":
        # Stableswap pool: "pool_liquidity"
        pool_liquidity = pool.get("pool_liquidity", [])
        for asset in pool_liquidity:
            denom = asset.get("denom", "")
            if denom == token_denom:
                return True

    elif pool_type == "/osmosis.concentratedliquidity.v1beta1.Pool":
        # Concentrated Liquidity pool: check "token0" and "token1"
        token0 = pool.get("token0", "")
        token1 = pool.get("token1", "")
        if token0 == token_denom or token1 == token_denom:
            return True

    elif pool_type == "/osmosis.cosmwasmpool.v1beta1.CosmWasmPool":
        # CosmWasm pool: decode instantiate_msg
        instantiate_msg_b64 = pool.get("instantiate_msg", "")
        if instantiate_msg_b64:
            try:
                decoded_msg = base64.b64decode(instantiate_msg_b64).decode("utf-8")
                msg_data = json.loads(decoded_msg)
                # Assumption: The keys might differ based on the contract logic
                base_denom = msg_data.get("base_denom", "")
                quote_denom = msg_data.get("quote_denom", "")
                if base_denom == token_denom or quote_denom == token_denom:
                    return True
            except Exception:
                # If decoding fails or doesn't match the expected structure, ignore
                pass

    return False

def get_pools_with_token(pools, token_denom):
    """
    Returns a list of dictionaries each containing 'id' and 'type' for pools that contain the token_denom.
    """
    matching_pools = []
    for pool in pools:
        pool_id = pool.get("id", None)
        if pool_id is None:
            # If a pool lacks an 'id' field, skip
            continue
        if pool_contains_token(pool, token_denom):
            pool_type = pool.get("@type", "")
            matching_pools.append({"id": pool_id, "type": pool_type})
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

    # Merge stderr into stdout
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

    # 1. Get the most recent all_pools file
    all_pools_file = get_most_recent_all_pools_file(SNAPSHOT_DIR)
    if not all_pools_file:
        return

    print(f"Using all pools file: {all_pools_file}")
    pools = load_pools(all_pools_file)

    # 2. Find pools that contain TOKEN_DENOM
    pools_with_token = get_pools_with_token(pools, TOKEN_DENOM)
    print(f"Found {len(pools_with_token)} pools containing '{TOKEN_DENOM}'")

    # Create a timestamp for naming files
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Write pools_for_<TOKEN_NAME>_<timestamp>.json with their types
    safe_token_name = TOKEN_DENOM.replace('/', '_')
    pools_for_token_file = os.path.join(SNAPSHOT_DIR, f"pools_for_{safe_token_name}_{timestamp}.json")
    with open(pools_for_token_file, "w") as f:
        json.dump(pools_with_token, f, indent=2)
    print(f"Pools for {TOKEN_NAME} saved to {pools_for_token_file}")

    # Track number of LPers for summary
    pool_owners_count = {}

    # 3. For each pool, run the denom-owners command
    for p in pools_with_token:
        pool_id = p["id"]
        pool_type = p["type"]
        denom = f"gamm/pool/{pool_id}"
        print(f"Fetching LP owners for pool {pool_id} ({pool_type}) (denom={denom})...")
        owners = fetch_pool_owners(denom)

        # Save LP owners to a timestamped file
        lp_filename = os.path.join(SNAPSHOT_DIR, f"lp_addresses_for_{TOKEN_NAME}_{pool_id}_{timestamp}.json")
        with open(lp_filename, "w") as f:
            json.dump(owners, f, indent=2)
        print(f"LP owners for pool {pool_id} saved to {lp_filename}")

        pool_owners_count[pool_id] = len(owners)

        time.sleep(0.2)

    # Print out summary
    print(f"\nThere are {len(pools_with_token)} pools with {TOKEN_NAME}")
    for p in pools_with_token:
        pid = p["id"]
        ptype = p["type"]
        count = pool_owners_count.get(pid, 0)
        print(f"pool {pid} ({ptype}) has {count} liquidity providers")

if __name__ == "__main__":
    main()
