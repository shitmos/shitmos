# Alchemy - turning shit into gold
Alchmey is the process of turning non-gold materials into gold.
Alchemy in the context of shitmos, is the process of turning shitmos into gold.
Bitcoin is digital gold.

### BTC/SHITMOS LP
The Shitmos Hub will set up a BTC/SHITMOS LP on Osmosis to facilitate this.
The pool will be a weighted pool, heavily weighted towards shitmos to flex the power of the shitmos hub's treasury in shitmos.

Alchemy inputs:
- initial BITCOIN quantity 0.00890047
- initial SHITMOS quantity 49,920

Pool details:
type: weighted pool
weight_bitcoin: 40%
weight_shitmos: 60%
swap fee: 0.222222%



### SHITMOS/BAG LP
While Baguette coin is not digital gold, it is digital food. If anything, food could be seen as a form of gold. According to Shitmos Hub proposal A12, if passed, a 111,111 SHITMOS/BAG LP will need to be created in the effort to make SHITMOS the liquidity center for meme coins in cosmos.

Alchemy inputs:
- initial BAG quantity 111,111
- shitmos initial quantity 24,740

weight_shitmos: 40%
weight_bag: 60%
swap fee: 0.222222%


### Basics of setting up a pool

This is the DAO DAO template when you look up the custom function `/osmosis.gamm.poolmodels.balancer.v1beta1.MsgCreateBalancerPool` and it's a good starting point.

```json
{
  "stargate": {
    "typeUrl": "/osmosis.gamm.poolmodels.balancer.v1beta1.MsgCreateBalancerPool",
    "value": {
      "sender": "",
      "poolAssets": [],
      "futurePoolGovernor": ""
    }
  }
}
```

stargate: 
typeUrl: This is the message type
value: this is the message itself

Value refers to the contents of the mesage. The contents are comprised of:
- sender
- poolAssets
- futurePoolGovernor