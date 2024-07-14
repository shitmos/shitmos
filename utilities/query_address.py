# DOES NOT WORK

import requests
import pandas as pd

def fetch_transactions(address, api_url):
    query = """
    query GetTransactions($address: String!) {
      events(where: {recipient: {_eq: $address}}, limit: 100) {
        block_height
        transaction_hash
        type
        attributes {
          key
          value
        }
      }
    }
    """
    variables = {"address": address}
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(api_url, json={'query': query, 'variables': variables}, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'data' not in data or 'events' not in data['data']:
            print("Data or events key missing in the response: ", data)
            return None
        return data
    else:
        print(f"Failed to fetch data: {response.status_code} {response.text}")
        return None

def summarize_funds_by_sender(transactions, address):
    if not transactions or 'data' not in transactions or 'events' not in transactions['data']:
        print("Invalid or incomplete transaction data received:", transactions)
        return {}

    funds_by_sender = {}

    for event in transactions['data']['events']:
        sender = None
        amount = 0
        for attribute in event['attributes']:
            if attribute['key'] == 'sender':
                sender = attribute['value']
            if attribute['key'] == 'amount' and 'uatom' in attribute['value']:
                amount += int(attribute['value'].split('uatom')[0])

        if sender and amount > 0:
            funds_by_sender[sender] = funds_by_sender.get(sender, 0) + amount

    return funds_by_sender

# Main script
address = "stars1r6f5tfxdx2pw5p94f2v5n96xd4nglz5qdgl4l3"
api_url = "https://constellations-api.mainnet.stargaze-apis.com/graphql"
transactions = fetch_transactions(address, api_url)

if transactions:
    funds_by_sender = summarize_funds_by_sender(transactions, address)
    if funds_by_sender:
        df = pd.DataFrame(list(funds_by_sender.items()), columns=['Sender', 'Total Amount Received (uatom)'])
        print(df)
    else:
        print("No funds transfers found.")
else:
    print("Failed to retrieve or process transactions.")
