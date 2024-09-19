import os
import json
from collections import defaultdict
from datetime import datetime
import requests
import urllib.parse

import config

# collection_addr can be declared up here
# shitmos would be stars1z2mxxjct3lmq6yndqx6e7sxuamc7t0k24y9jq3y907vmg2wwt4rs7klax9
# shitzilla is stars1vpc22a2n4cglxwmndm4gf0ksqcwf39232kxwz0m67ntp4eda4ahsfdj9gm


def load_json(filename):
    with open(filename, 'r') as fp:
        json_data = json.load(fp)
        return json_data


def save_json(filename, out_dict, **kwargs):
    with open(filename, 'w') as fp:
        json.dump(out_dict, fp, indent=2, ensure_ascii=False, **kwargs)
        return out_dict


def parse_request():
    """
    Helper function for construct parameters in request
    """

    encoded_parameters = "parameters=%5B%7B%22type%22%3A%22category%22%2C%22value%22%3A%22" \
                         "stars1z2mxxjct3lmq6yndqx6e7sxuamc7t0k24y9jq3y907vmg2wwt4rs7klax9%22%2C%22id%22%3A%22" \
                         "cb34b7a8-70cf-ba86-8d9c-360b5b2fedd3%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22" \
                         "template-tag%22%2C%22collection_addr%22%5D%5D%7D%5D"
    decoded_parameters = urllib.parse.unquote(encoded_parameters)
    print(decoded_parameters)


def request_holders():
    url = "https://metabase.constellations.zone/api/public/card/4cf9550e-5eb7-4fe7-bd3b-dc33229f53dc/query/json"
    collection_addr = "stars1z2mxxjct3lmq6yndqx6e7sxuamc7t0k24y9jq3y907vmg2wwt4rs7klax9"

    parameters = [{"type": "category",
                   "value": collection_addr,
                   "id": "cb34b7a8-70cf-ba86-8d9c-360b5b2fedd3",
                   "target": ["variable", ["template-tag", "collection_addr"]]
                   }]
    encoded_parameters = json.dumps(parameters)
    response = requests.get(url, params={"parameters": encoded_parameters})

    return response.json()


def make_snapshot(force=False):
    today = datetime.now().strftime("%Y-%m-%d")
    out_filename = os.path.join(config.SNAPSHOTS_FOLDER, f"snapshot_{today}.json")
    if os.path.exists(out_filename) and not force:
        holders_data = load_json(out_filename)
        print(f"Load snapshot from {out_filename}")
    else:
        holders_data = request_holders()
        save_json(out_filename, holders_data)
        print(f"Collect new snapshot to {out_filename}")
    return holders_data


def calculate_holders(*, include_listed: bool):
    snapshot_data = make_snapshot()
    holders_data = defaultdict(int)
    for nft_data in snapshot_data:
        if not include_listed and nft_data['is_listed']:
            continue
        holders_data[nft_data['owner_addr']] += 1
    return dict(holders_data)


if __name__ == '__main__':
    ret = calculate_holders(include_listed=config.INCLUDE_LISTED_NFT_FOR_DISTRIBUTE)
