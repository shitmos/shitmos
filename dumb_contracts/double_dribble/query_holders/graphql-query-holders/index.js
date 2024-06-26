import fetch from 'cross-fetch'; // Ensure this is at the top if you're using Node.js
import { ApolloClient, InMemoryCache, gql, HttpLink } from '@apollo/client/core/core.cjs';


const client = new ApolloClient({
    link: new HttpLink({
        uri: 'https://graphql1.mainnet.stargaze-apis.com/graphql',
        fetch: fetch
    }),
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

    getTraitsAndOwner('stars1z2mxxjct3lmq6yndqx6e7sxuamc7t0k24y9jq3y907vmg2wwt4rs7klax9','2186')
    .then(result => console.log(result.data))
    .catch(error => console.error(error));