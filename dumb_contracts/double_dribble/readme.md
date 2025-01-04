# double dribble
simple way to send shitmos from collection wallet to nft holders. these will be performed by the shitmos nft wallet:

osmo1c7gsk4eaelpcplg0j5urpwnzqrp6wnyt9uexy6 - this is the admin address
stars1c7gsk4eaelpcplg0j5urpwnzqrp6wnytematee - not sure what this address does

so as to not send shitmos from SEZ member collections to nft holders.

The sender if default doubled_dribble:
KEY_NAME = "shitmos_nft"
WALLET_NAME = "Shitmos NFT Wallet"


# where is all the stuff

you want to go to the `code` folder to run this
in the `code` folder there is a file `double_dribble.sh` this is the main script
to quick run, if configuration is set up correctly... run the following commands
from the root directory

```bash
cd ~/repos/shitmos/dumb_contracts/double_dribble/code
./double_dribble.sh
```
# if you need to set up a wallet

`osmosisd keys add <name of new key> --recover`

# steps

1. get list of holders (exclude listed nfts) and their quantities
- this is done with 

2. convert addresses to osmo addresses

3. use modified version of shitdribble code to bulk send shitmos to all holders of unlisted nfts:

4. calculate remaining amount from 2222 x 2.22 = 4,932.84 as "dingleberries" to be rolled into a special wallet that will be distributed to a random trait each "random interval"

amount_per_nft = number of shitmos each nft receives

amount_held_by_wallet = number of nfts held by each wallet

amount_per_nft * amount_held_by_wallet is the amount to send for each wallet in the list.

execute the code by running:
`./double_dribble.sh`

### Todos

1. figure out a way to ensure shitmos is sent to dao wallets - need some other way to:
    1. identify a dao wallet
    2. match it's OSMO equivalent address (if it exists)
        1. If DAO hasn't set up cross-chain Osmo account -> join the DAO and submit a governance proposal
        2. Once gov proposal passes, grab their Osmo address

### troubleshooting
errors with signing:
