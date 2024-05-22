
# to get the wallet balances in a nice readable format
python3 get_wallet_balances.py sez --keyring-backend file

# to send exact amount to all members
cd ~/repos/shitmos/token/shitdribble
export OSMOSISD_KEYRING_BACKEND=file
chmod +x shitdribble.sh
./shitdribble.sh

# to check on a transaction hash
osmosisd query tx <transaction hash> --output json | jq .

osmosisd query tx 2167192F411CB3B99291411FE342327AC34661D04D7C52D6056955E78E2EC9A7 --output json | jq .
osmosisd query tx E223847D91141D9940E786C6CFACF7965500CBCB425AF708F31E19250FAB0A3B --output json | jq .
osmosisd query tx D5916BED0442031A01737D04A4A59BBBB06D0C369F601DE21C6524157106346E --output json | jq .