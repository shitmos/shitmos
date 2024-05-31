import json
import requests

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

collection_address = config['collection_address']

def get_nft_holders(collection_address):
    holders = []
    url = "https://graphql.mainnet.stargaze-apis.com/graphql"
    headers = {"Content-Type": "application/json"}

    # GraphQL query to fetch tokens
    query_tokens = json.dumps({
        "query": f"""
        query GetTokens {{
            tokens(collectionAddr: "{collection_address}") {{
                tokens {{
                    tokenId
                }}
            }}
        }}
        """
    })

    # Send request to the GraphQL endpoint
    response_tokens = requests.post(url, data=query_tokens, headers=headers)
    if response_tokens.status_code != 200:
        print("Failed to fetch tokens:", response_tokens.text)
        return []

    tokens_data = response_tokens.json()
    tokens = tokens_data['data']['tokens']['tokens']
    for token in tokens:
        token_id = token['tokenId']
        # GraphQL query to get the owner of each token
        query_owner = json.dumps({
            "query": f"""
            query GetOwner {{
                token(collectionAddr: "{collection_address}", tokenId: "{token_id}") {{
                    owner {{
                        address
                    }}
                }}
            }}
            """
        })
        response_owner = requests.post(url, data=query_owner, headers=headers)
        if response_owner.status_code == 200:
            owner_data = response_owner.json()
            owner_address = owner_data['data']['token']['owner']['address']
            holders.append(f"Token ID: {token_id}, Owner: {owner_address}")
        else:
            print("Failed to fetch owner for token", token_id, "Error:", response_owner.text)

    return holders

# Get NFT holders
nft_holders = get_nft_holders(collection_address)

# Write results to a file
with open('nft_holders.txt', 'w') as f:
    for line in nft_holders:
        f.write(line + '\n')

print("NFT holder information written to 'nft_holders.txt'.")
