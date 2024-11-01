# dump

A `dump` is a `dumb_contract` that distributes a digital asset to wallets that are required to hold digital assets from at least 2 different nft collections. `dumps`are currently only supported on the Stargaze blockchain, but more support can be added over time

# how to do a dump

STEP 1 - Create and setup subdirectory for the dump

```bash
cd dumb_contracts/dump
mkdir <dump_name>
cd <dump_name>
touch collections.txt
echo "name, address" > collections.txt
```
then in `collections.txt` put the name, collection_address for each of the collections.
this can be plugged into some sort of automation in the future


STEP 2 - Update configuration variables from `double_dribble`

What denom to distribute in `config.py`
Quantity per matching set in `config.py`
Location that snapshots should go `SNAPSHOTS_FOLDER` in `config.py`

STEP 3 - Run snapshots for each of the collection addresses

`python3 ../../double_dribble/code/snapshots.py`

> note you can print the context of `collections.txt` by running `cat collections.txt`





A `dump` uses a lot of the tools from `double_dribble` another dumb contract.

Choose the collections that you want to snapshot
Create the snapshots of those collections by using `snapshots.py` from `../double_dribble/code/snapshots.py`
To automate this from the `dump` subdirectory:

STEP 1 - HOW TO RUN `snapshots.py`
1. navigate to the `dump` subdirectory `cd dumb_contracts/dump`
2. run `snapshots.py` from this subdirectory with `python3 ../double_dribble/code/snapshots.py`

STEP 2 - CONFIGURE `snapshots.py` FOR COLLECTIONS YOU WANT TO SNAPSHOT
1. open the `snapshots.py` file and change the `collection_addr` variable to the contract address of the first of the collections you want to snapshot
2. also need to change the `SNAPSHOTS_FOLDER` in `config.py` to the `dump` subdirectory associated with the relevant grouping of collections
- for example, say you wanted to snapshot all of the holders of all of the collections created by a specific artist, you might want to create a subdirectory named after that artist, or if you wanted to snapshot all of the holders of all of the collections in a specific ecosystem.
- hmmmm... this gets me thinking.

NEW STEP 1 - Create and setup subdirectory for the dump

tests

```bash
cd shitmos/dumb_contracts/dump
mkdir test
cd test
touch collections.txt
echo "name, address" > collections.txt
```