# double dribble
simple way to send shitmos from collection wallet to nft holders. these will be performed by the shitmos nft wallet:

osmo1c7gsk4eaelpcplg0j5urpwnzqrp6wnyt9uexy6
stars1c7gsk4eaelpcplg0j5urpwnzqrp6wnytematee

so as to not send shitmos from SEZ member collections to nft holders.

# steps

1. get list of holders and their quantities



2. convert addresses to osmo addresses

3. use modified version of shitdribble code to bulk send shitmos to all holders:

amount_per_nft = number of shitmos each nft receives

amount_held_by_wallet = number of nfts held by each wallet

amount_per_nft * amount_held_by_wallet is the amount to send for each wallet in the list.

execute the code by running:
`./double_dribble.sh`

