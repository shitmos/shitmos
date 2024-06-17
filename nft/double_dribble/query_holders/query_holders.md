# how to query holders


# stargaze api

Stargaze has a GraphQL API that can be used to query the holders of an nft collection. I've tried using it with very limited success, due to my inexperience and lack of knowledge with graphQL.

https://docs.stargaze.zone/developers/stargaze-api

I managed to get a query working to retrieve the addresses for 100 holders, but couldn't figure out pagiation. The query also was very slow.

The stargaze api page linked above provides an example usage of their GraphQL api, but doesn't explain how it works, so you basically just need to be a real developer to use it.

```javascript
import { ApolloClient, InMemoryCache, gql } from '@apollo/client';

const client = new ApolloClient({
	uri: 'https://graphql.mainnet.stargaze-apis.com/graphql',
	cache: new InMemoryCache(),
});

const getTraitsAndOwner = (collectionAddr, tokenId) =>
	client.query({
		query: gql`
            query Query {
                token(
                    collectionAddr: "${collectionAddr}"
                    tokenId: "${tokenId}"
                ) {
                    traits {
                        name
                        value
                    }
                    owner {
                        address
                        name {
                            name
                        }
                    }
                }
            }
        `,
    });
```

It looks like to use it you need to have node js installed and you need to initialize a node project. lets go through those steps:

`mkdir graphql-query-holders`
`cd graphql-query-holders`
`npm init -y`
`npm install @apollo/client graphql`
`touch index.js`

There will be a `package.json` file that needs some additional configuration. Sepcifically, will need to add:

`"type": "module",` at the top.

Paste the above code and include:

```javascript
getTraitsAndOwner('collection_address','token_id')
    .then(result => console.log(result.data))
    .catch(error => console.error(error));
```

We will go for one of the shitmos nfts with some interesting properties. I filtered the collection for PBJ = Yes and Frog Day = Yes which gave me only 12 results. I like the aesthetics of id #2186 so let's use that as a test.

![Shitmos NFT ID 2186](image.png)

The shitmos nft collection address is: `stars1z2mxxjct3lmq6yndqx6e7sxuamc7t0k24y9jq3y907vmg2wwt4rs7klax9`
And the id of the specific nft is:
`2186`

Run the code with `node index.js`
Get a bunch of error messages, get stuck in dependency hell, and then give up on this part for the time being.

# because you don't know how to use graphql / node
Switch to the manual route to get a collection snapshot.
Go to:
https://studio.stargaze.zone/snapshots/

And insert the collection address in the "Collection Address" box:
`stars1z2mxxjct3lmq6yndqx6e7sxuamc7t0k24y9jq3y907vmg2wwt4rs7klax9`

Then, uncheck "include tokens listd on Marketplace" so that the collectors receive the double_dribbe.