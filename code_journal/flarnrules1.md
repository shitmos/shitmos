### July 13, 2024 -
To dos:
1. [ ] set up dingleberry basics, even if manual
2. [x] send 222 bounty for videos of dingleberry traits
3. [ ] submit cosmos chain registry pull request to get shitmos on stargaze
4. [ ] change the proposal deposit from 100 stars to 2 shitmos
5. [ ] submit proposal to add the press widget
6. [ ] create a cryptocurrency staking DAO - The Shitmos Hub
7. [ ] query on-chain data from addresses by address
8. [ ] figure out price retrieval for shitmos token in a DAO DAO treasury

#### 6 set up dingleberry basics, even if manual

python script `generate_dingleberry.py`
1. Identify the specific ids of nfts based on two inputs: trait_type and value

2. Then, the wallets associated with those ids should split evenly the contents of the dingleberry wallet

procedure
1. spin the wheels, or have someone spin the wheels
2. announce criteria on Discord alpha channel
3. announce criteria on Discord public channel
4. announce criteria on Telegram
5. announce criteria on Twitter
6. wait some more days
7. do a couple double_dribbles
8. start a 24 hour countdown
9. release the dingleberries
10. spin the wheels or have someone spin the wheels

annoucements can be in the form of video capture of the wheel spins.

#### 5 submit proposal to add the press widget
just tried to submit a proposal to add the press widget and the transaction failed
the transaction gave me this error message:![alt text](image.png)
`Signature verification failed. Try again in 10 seconds or reach out to us on Discord for help.`

1. [X] reach out on discord
2. [ ] follow up

#### 7 query funds received from addresses by address

I need a name for this, can go in utilities
query_address.py

```python
import subprocess
import json
import pandas as pd

# Function to get transactions for a given address
def get_transactions(address):
    command = f"starsd query txs --events 'transfer.recipient={address}' --output json"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    transactions = json.loads(result.stdout)
    return transactions

# Function to parse transactions and summarize funds received by sender
def summarize_funds_by_sender(transactions, address):
    funds_by_sender = {}

    for tx in transactions['txs']:
        for event in tx['events']:
            if event['type'] == 'transfer':
                attributes = event['attributes']
                sender = None
                amount = None

                for attribute in attributes:
                    if attribute['key'] == 'sender':
                        sender = attribute['value']
                    if attribute['key'] == 'amount':
                        amount = attribute['value']

                if sender and amount:
                    if sender not in funds_by_sender:
                        funds_by_sender[sender] = 0
                    funds_by_sender[sender] += int(amount.split('uatom')[0])  # Assuming the denomination is uatom

    return funds_by_sender

# Main script
address = "your_stargaze_address_here"
transactions = get_transactions(address)
funds_by_sender = summarize_funds_by_sender(transactions, address)

# Convert to DataFrame for better visualization
df = pd.DataFrame(list(funds_by_sender.items()), columns=['Sender', 'Total Amount Received (uatom)'])
print(df)

```