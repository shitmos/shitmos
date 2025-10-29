### some basic commands

cd repos
git clone https://github.com/osmosis-labs/osmosis-installer
cd ~/repos/osmosis-installer
chmod +x osmosis-installer.sh



chmod +x flydrop.sh
./flydrop.sh

DEBUG=1 ./flydrop.sh


osmosisd keys add flydrop --recover --keyring-backend os
osmosisd keys show flydrop -a
osmosisd q bank balances osmo1q0tks0n67fthhu2pyw9xjfm9qk36hhky3xh9w0 --node https://osmosis-rpc.publicnode.com:443

### some gud commands

python3.11 flydrop.py \
  --from-key flydrop \
  --amount 1 \
  --denom uosmo \
  --dry-run

python3.11 flydrop.py \
  --input addresses.txt \
  --from-key flydrop \
  --keyring-backend file \
  --amount 100 --denom uosmo \
  --chain-id osmosis-1 \
  --node https://rpc.osmosis.zone:443 \
  --gas-prices 0.025uosmo \
  --yes