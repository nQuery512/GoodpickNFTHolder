# GoodpickNFTHolder
Get NFT holder from a token-id list on Solana


## Requirement

Tested with python3.9 and solana python lib ver:0.15.1

```
pip install solana && pip install pandas
```

For now you need to put all token id that you got from
https://tools.abstratica.art/
into a file named "full.txt"

Will update soon to request abstratica directly

Then just run
```
python get_holder_from_list.py
```

Holder adresses are written into a file named final.json
