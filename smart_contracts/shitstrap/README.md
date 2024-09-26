# testing environment

## Step 1: go to test-net dao-dao actions page
connect wallet to: https://testnet.daodao.zone/actions

## Step 2: Make sure you are connected to the correct blockchain
Near the top right corner, click on the chain dropdown menu to switch chain, and select **Osmosis Testnet**

## Step 3: start a new "execute smart contract" message
in the Action Library, go to **Smart Contracting**
In **Smart Contracting** select **Execute Smart Contract**

## Step 4: Call the shitstrap contract
In smart contract address, put in the shitstrap contract address:
`osmo10jsnt4rhfsr7w50z3vg3ghfxy98fassnsxnmdypfuvnzzhscsegqsf9432`

## Step 5: Prepare the message

The format of the message is:

```json
{
    "shit_strap": 
    {
        "shit":  
        {
            "denom": 
            {
                "native": "factory/osmo1vpudlpnuqwlpuc2q9yptjssp46snvf2twu3t2s/shitstrap2"
            },  
            "amount": "69"
        }
    }
}
```

**Definitions for the objects in the above message:**
- `shit_strap` - name of message
- `shit` - token  you are depositing, consists of a `denom` and an `amount`
- `denom` - the denomination, or full name of the token you are deposting into the contract
- `amount` - quantity of token  you are depositing

## Step 6: Fund your deposit
Click on the **Add payment** button.
Select the coin  you are depositing - ensure you are depositing the denom of the coin listed in the message, so in this case it is the test token `factory/osmo1vpudlpnuqwlpuc2q9yptjssp46snvf2twu3t2s/shitstrap2`

## Step 7: Execute the deposit
Click execute.

If formatted correctly you will receive whatever amount of the base denom that has been encoded in the shitstrap contract.


