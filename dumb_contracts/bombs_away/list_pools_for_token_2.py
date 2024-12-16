import os
import json
import base64
import datetime

# Configuration: Set the token denom you're interested in
TOKEN_DENOM = "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/shitmos"  # Replace this with your desired denom
SNAPSHOT_DIR = "pool_snapshots"

def get_most_recent_snapshot(directory):
    files = [f for f in os.listdir(directory) if f.startswith("all_pools_") and f.endswith(".json")]
    if not files:
        print("No snapshot files found.")
        return None
    files.sort()  # due to naming, last in sort is the most recent
    return files[-1]

def load_pools(filename):
    path = os.path.join(SNAPSHOT_DIR, filename)
    with open(path, "r") as f:
        data = json.load(f)
    return data  # should be a list of pool objects

def pool_contains_token(pool, token_denom):
    pool_type = pool.get("@type", "")

    if pool_type == "/osmosis.gamm.v1beta1.Pool":
        # Vanilla GAMM pool: uses "pool_assets"
        pool_assets = pool.get("pool_assets", [])
        for asset in pool_assets:
            token = asset.get("token", {})
            denom = token.get("denom", "")
            if denom == token_denom:
                return True

    elif pool_type == "/osmosis.gamm.poolmodels.stableswap.v1beta1.Pool":
        # Stableswap pool: uses "pool_liquidity"
        pool_liquidity = pool.get("pool_liquidity", [])
        for asset in pool_liquidity:
            denom = asset.get("denom", "")
            if denom == token_denom:
                return True

    elif pool_type == "/osmosis.concentratedliquidity.v1beta1.Pool":
        # Concentrated Liquidity pool: has "token0" and "token1"
        token0 = pool.get("token0", "")
        token1 = pool.get("token1", "")
        if token0 == token_denom or token1 == token_denom:
            return True

    elif pool_type == "/osmosis.cosmwasmpool.v1beta1.CosmWasmPool":
        # CosmWasm pool: decode instantiate_msg to check tokens
        instantiate_msg_b64 = pool.get("instantiate_msg", "")
        if instantiate_msg_b64:
            try:
                decoded_msg = base64.b64decode(instantiate_msg_b64).decode("utf-8")
                msg_data = json.loads(decoded_msg)
                # Adjust keys based on actual contract logic if needed
                base_denom = msg_data.get("base_denom", "")
                quote_denom = msg_data.get("quote_denom", "")
                if base_denom == token_denom or quote_denom == token_denom:
                    return True
            except Exception:
                # If decoding fails or doesn't match expected structure, ignore
                pass

    return False

def main():
    # Find the most recent snapshot file
    most_recent_file = get_most_recent_snapshot(SNAPSHOT_DIR)
    if not most_recent_file:
        return

    print(f"Using snapshot file: {most_recent_file}")

    # Load all pools
    pools = load_pools(most_recent_file)

    # Find all pools that contain the given token denom
    pools_with_token = []
    for pool in pools:
        pool_id = pool.get("id", None)
        if pool_id is None:
            # If there's no id field, skip
            continue
        if pool_contains_token(pool, TOKEN_DENOM):
            pool_type = pool.get("@type", "")
            pools_with_token.append({"id": pool_id, "type": pool_type})

    print(f"Found {len(pools_with_token)} pools containing '{TOKEN_DENOM}'")

    for p in pools_with_token:
        print(f"Pool {p['id']} ({p['type']})")

    # Save the results to a timestamped JSON
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Replace '/' in TOKEN_DENOM for filename safety
    safe_token_name = TOKEN_DENOM.replace('/', '_')
    output_filename = os.path.join(SNAPSHOT_DIR, f"pools_for_{safe_token_name}_{timestamp}.json")
    with open(output_filename, "w") as f:
        json.dump(pools_with_token, f, indent=2)

    print(f"Pools for {TOKEN_DENOM} saved to {output_filename}")

if __name__ == "__main__":
    main()
