# shitmos
Cosmos network's premier self-hatred shitcoin

# CLI tools
This repo has code that utilize the stargaze and osmosis command line interface tools `starsd` and `osmosisd`

In order to use these tools, you will need to run a full node locally or connect to a public RPC.

Osmosis public RPC is: `https://rpc.osmosis.zone:443`

To test that it works, you can run this command:
`osmosisd query bank balances <any-osmosis-address> --node https://rpc.osmosis.zone:443`

If you don't want to write out the public node every time, you can add the node to the config file, which if you did a standard setup will be located here:
`~/.osmosisd/config/config.toml`

and then scroll down and replace whatever is in `laddr =` to:
`laddr = https://rpc.osmosis.zone:443`
