# bombs away
query osmosis and perform airdrop based on criteria

## query holders of a token

run
`python3 print_holders.py`


## using osmosis CLI

`osmosisd q bank denom-owners factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/shitmos --node https://rpc.osmosis.zone --page-limit 2000 -o json > output.json 2>&1`

`osmosisd q bank denom-owners factory/osmo1n6asrjy9754q8y9jsxqf557zmsv3s3xa5m9eg5/uspice --node https://rpc.osmosis.zone --page-limit 2000 -o json > output.json 2>&1`

## using osmosis CLI for pools

pools
`osmosisd q gamm pools --node https://rpc.osmosis.zone` <- this only gives you gamm style pools

all pools
`osmosisd query poolmanager all-pools --node https://rpc.osmosis.zone` <- this gives you more than just gamm style

holders of a pool
`osmosisd q bank denom-owners gamm/pool/1 --node https://rpc.osmosis.zone --page-limit 10000 -o json > lp_list.json 2>&1`

### poolmanager
starting stub of command:
`osmosisd query poolmanager [command]`

some interesting commands:
`all-pools` gives you all of the pools
`total-pool-liquidity` -> `[pool-id] [flags]`
`total-volume-for-pool`
`spot-price`

### potential way to calculate volume
start here:
`osmosisd query poolmanager total-volume-for-pool`

then work this into a script that runs this command for a whole bunch of different block heights, and then calculate the deltas.

block height can be chosen with the `height int` command
we can sort of figure out stuff about epochs by running `osmosisd query epochs epoch-infos` but this doesn't quite get us there...

## if internet connection is bad, run this

`sudo cp /etc/resolv.conf /etc/resolv.conf.backup`
`sudo nano /etc/resolv.conf`

change nameserver to:
`8.8.8.8` -> google
`8.8.4.4` -> google alt
or
`1.1.1.1` -> cloudflare
`1.0.0.1` -> cloudflare alt



# querying transactions
start with:
`osmosisd query txs --query [string]` the string must comform to Tendermint's query semantics.
