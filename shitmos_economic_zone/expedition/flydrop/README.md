# Flydrop (double_dribble-style)

## Setup
- Ensure osmosisd on PATH
- Import your key into the **file** keyring (so prompts show in terminal):
  osmosisd keys add flydrop --recover --keyring-backend file

- Python deps:
  pip install bech32

## Files
- flydrop.sh              ← main driver
- generate_flydrop.py     ← unsigned tx generator (chunked)
- addresses.txt           ← input list (stars1... or osmo1...)

## Run
chmod +x flydrop.sh
./flydrop.sh

## Verbose Run
DEBUG=1 ./flydrop.sh

## Balance check
osmosisd q bank balances osmo1q0tks0n67fthhu2pyw9xjfm9qk36hhky3xh9w0 --node https://osmosis-rpc.publicnode.com:443


The script will:
1) Save inputs and initial balances to flydrops/flydrop_000N/
2) Generate unsigned tx JSONs (1 per chunk, many MsgSend per tx)
3) Prompt you to sign each (file keyring passphrase shows) and broadcast
4) Save broadcast results, final balances
















# shitmos airdrop for expedition stamps holders
222 stamps in the expedition collection have a fly attribute.
holders of this attribute will receive an airdrop of shitmos

wallet utilized to perform airdrop:
new wallet


shitmos airdrop sponsors:
1. flarnrules - 22 per holder ~ 4884 shitmos
2. 

## HOW TO USE

1. put your list in `addresses.txt` or pass `--input <file>`
2. confirm credentials `osmosisd keys show flydrop -a`
3. dry-run `python3.11 flydrop.py --from-key flydrop --amount 1 --denom uosmo --dry-run --max 5`
4. go live (example):
```bash
python3.11 flydrop.py --from-key flydrop \
  --amount 164280 --denom upleb \
  --chain-id osmosis-1 --node https://rpc.osmosis.zone:443 \
  --gas-prices 0.025uosmo --yes --sleep 0.4 --memo "flydrop"
```