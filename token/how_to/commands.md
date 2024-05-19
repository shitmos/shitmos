
# to get the wallet balances in a nice readable format
python3 get_wallet_balances.py sez --keyring-backend file

# to send exact amount to all members
cd ~/repos/shitmos/token/scripts
export OSMOSISD_KEYRING_BACKEND=file
chmod +x shitdribble.sh
./shitdribble.sh

# to check on a transaction hash
osmosisd query tx <transaction hash> --output json | jq .

osmosisd query tx 2167192F411CB3B99291411FE342327AC34661D04D7C52D6056955E78E2EC9A7 --output json | jq .