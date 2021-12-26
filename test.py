from web3.middleware import geth_poa_middleware
from service.sync import process_transactions
from web3 import Web3, HTTPProvider
import config
import json

w3 = Web3(HTTPProvider(config.endpoint))

if config.testnet:
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

print(json.dumps(process_transactions(w3, 6085036), indent=4))
