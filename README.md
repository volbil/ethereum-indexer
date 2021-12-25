# Simple Ethereum indexer

Quick and dirty indexer for Ethereum transactions.

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
