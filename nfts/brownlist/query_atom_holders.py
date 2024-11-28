import requests
import json

# Constants
API_URL = "https://api.mintscan.io/v1/cosmos/accounts/richlist/uatom"
THRESHOLD_ATOM = 22

# Load API Key
with open('../../api/mintscan.txt', 'r') as file:
    API_KEY = file.read().strip()

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def convert_uatom_to_atom(uatom):
    return uatom / 1000000

def safe_json_parse(response):
    try:
        return response.json()
    except json.JSONDecodeError:
        print("Failed to decode JSON:", response.text)
        return None

def get_richlist(page_token=None):
    params = {
        "take": 100,  # Adjust as needed, default is 20
        "detail": True
    }
    if page_token:
        params["searchAfter"] = page_token
    
    response = requests.get(API_URL, headers=headers, params=params)
    
    # Debugging: Print the request details
    print("Request URL:", response.url)
    print("Request Headers:", response.request.headers)
    print("Response Status Code:", response.status_code)
    print("Response Text:", response.text)
    
    if response.status_code != 200:
        print("Failed to fetch data:", response.status_code, response.text)
        return None
    return safe_json_parse(response)

def main():
    accounts_above_threshold = []
    page_token = None

    while True:
        richlist = get_richlist(page_token)
        if not richlist or "accounts" not in richlist:
            break

        for account in richlist["accounts"]:
            balance = int(account.get('balance', 0))
            atom_balance = convert_uatom_to_atom(balance)
            if atom_balance > THRESHOLD_ATOM:
                accounts_above_threshold.append(f"Address: {account['address']}, Balance: {atom_balance} ATOM")
        
        if "pagination" in richlist and "next_key" in richlist["pagination"]:
            page_token = richlist["pagination"]["next_key"]
        else:
            break

    with open("accounts_above_22_atom.txt", "w") as file:
        for account in accounts_above_threshold:
            file.write(account + "\n")

    print(f"Saved {len(accounts_above_threshold)} accounts to accounts_above_22_atom.txt")

if __name__ == "__main__":
    main()
