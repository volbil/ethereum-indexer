# Simple Ethereum indexer

Quick and dirty indexer for Ethereum transactions.

## Requests

Address history:

```
/v1/history/0x3c2c9449eba4db4e0e62726c84de145dfbf0a5a6?page=1
```

Transaction info:

```
/v1/transaction/0xcdcca77ccdb296da08830c577aaca0fc0bbf072ea7713a8c000af440e7c64aae
```

## Config

Config example:

```python
endpoint = "http://127.0.0.1:9999"
start_hash = "0x4070218da4aa535ae3194949be97f0f381f21a3cf51bbc94afa2661a73d1c269"
start_height = 6061155
testnet = True

contracts = [
    {
        "address": "CONTRACT_ADDRESS",
        "ticker": "TICKER",
        "name": "Token",
        "decimals": 18
    }
]

db = {
    "provider": "sqlite",
    "filename": "../local.db",
    "create_db": True
}
```
