# Cosmos Chain Registry
Cosmos network has a chain registry that is like the centerpoint for all assets and blockchains in the cosmos network.
The repo exists here:
https://github.com/cosmos/chain-registry

# Shitmos on the chain registry
Shitmos needs to have it's various token details listed on the chain registry to be recognized.

when shitmos made it out of the Liquidity Bootstrapping Pool (LBP) on start.cooking a pull request (PR) was automatically made to incorporate shitmos into the chain registry for Osmosis. This is the json data that resides on the chain registry:

```json
    {
      "description": "Like cosmos, but shit",
      "denom_units": [
        {
          "denom": "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/shitmos",
          "exponent": 0
        },
        {
          "denom": "SHITMOS",
          "exponent": 6
        }
      ],
      "type_asset": "sdk.coin",
      "address": "osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8",
      "base": "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/shitmos",
      "name": "Shitmos",
      "display": "SHITMOS",
      "symbol": "SHITMOS",
      "logo_URIs": {
        "png": "https://raw.githubusercontent.com/cosmos/chain-registry/master/osmosis/images/SHITMOS.png"
      },
      "images": [
        {
          "png": "https://raw.githubusercontent.com/cosmos/chain-registry/master/osmosis/images/SHITMOS.png"
        }
      ]
    },
```

As shitmos spreads across the cosmos, more entries need to be made to enhance the user experienc when dealing with the shitmos coin.
Shitmos had a governance proposal passed to be added to a set of whitelist assets on Migaloo chain. Here's the draft of the chain registry entry for Migaloo

```json
    {
      "denom_units": [
        {
          "denom": "ibc/0E1B883A15D5FCA533332CBAB1A672934C3936920399F2A3EB4F438E3EBAD0E9",
          "exponent": 0,
          "aliases": [
            "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/shitmos"
          ]
        },
        {
          "denom": "shitmos",
          "exponent": 6
        }
      ],
      "type_asset": "ics20",
      "base": "ibc/0E1B883A15D5FCA533332CBAB1A672934C3936920399F2A3EB4F438E3EBAD0E9",
      "name": "Shitmos",
      "display": "Shitmos",
      "symbol": "SHITMOS",
      "traces": [
        {
          "type": "ibc",
          "counterparty": {
            "chain_name": "osmosis",
            "base_denom": "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/shitmos",
            "channel_id": "channel-642"
          },
          "chain": {
            "channel_id": "channel-5",
            "path": "transfer/channel-5/factory/factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/shitmos"
          }
        }
      ],
      "images": [
        {
          "image_sync": {
            "chain_name": "osmosis",
            "base_denom": "factory/osmo1q77cw0mmlluxu0wr29fcdd0tdnh78gzhkvhe4n6ulal9qvrtu43qtd0nh8/shitmos"
          },
          "png": "https://raw.githubusercontent.com/cosmos/chain-registry/master/migaloo/images/shitmos.png",
          "svg": "https://raw.githubusercontent.com/cosmos/chain-registry/master/migaloo/images/shitmos.svg"
        }
      ],
      "logo_URIs": {
        "png": "https://raw.githubusercontent.com/cosmos/chain-registry/master/migaloo/images/shitmos.png",
        "svg": "https://raw.githubusercontent.com/cosmos/chain-registry/master/migaloo/images/shitmos.svg"
      }
    }
```
It is important that this information is accurate, as it is the "under the hood" wiring for recognition on Migaloo to allow people to use Shitmos as a restake asset.