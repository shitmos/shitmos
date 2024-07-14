# double dribble
simple way to send shitmos from collection wallet to nft holders. these will be performed by the shitmos nft wallet:

osmo1c7gsk4eaelpcplg0j5urpwnzqrp6wnyt9uexy6
stars1c7gsk4eaelpcplg0j5urpwnzqrp6wnytematee

so as to not send shitmos from SEZ member collections to nft holders.

# steps

1. get list of holders (exclude listed nfts) and their quantities

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
