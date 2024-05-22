# shitdribble steps

1. update `collections.js` to make sure you have all of the collections you want to shitdribble and if each collection is multiple wallets, ensure you have the proper weights
2. in `token/scripts` run `python3 convert_addresses.py` to create the osmosis version of a specific wallet's stars address
3. look at `config.py` and determine how much, of what, you want to shitdribble to the various recipients
4. if your config is all set up, you merely have to run the below command (doesn't even matter what your `pwd` is because it will take you to the correct directory)

```
cd ~/repos/shitmos/token/shitdribble
export OSMOSISD_KEYRING_BACKEND=file
chmod +x shitdribble.sh
./shitdribble.sh
```
