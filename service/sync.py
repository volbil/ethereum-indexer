from web3.middleware import geth_poa_middleware
from web3 import Web3, HTTPProvider
from .models import Transaction
from datetime import datetime
from .models import Contract
from .models import Address
from .models import Block
from pony import orm
import config
import math

DECIMALS = 18

def log_message(message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now} {message}")

def amount(value, decimals):
    return round(float(value) / math.pow(10, decimals), decimals)

def process_transactions(w3, height):
    txs = w3.eth.getBlockTransactionCount(height)
    result = []

    for index in range(0, txs):
        tx = w3.eth.getTransactionByBlock(height, index)
        receipt = w3.eth.getTransactionReceipt(tx["hash"])

        gasused = receipt["gasUsed"]
        gasprice = tx["gasPrice"]
        contract = "NO_CONTRACT"
        txid = tx["hash"].hex()
        value = tx["value"]
        sender = tx["from"]
        receiver = tx["to"]
        data = tx["input"]
        token = False

        # Check if transaction is a contract transfer
        if (tx["value"] == 0 and not data.startswith("0xa9059cbb")):
            continue

        if not sender or not receiver:
            continue

        if data.startswith("0xa9059cbb"):
            contract_to = "0x" + data[10:-64][-40:]

            contract = receiver
            receiver = contract_to

            if len(contract_to) > 128:
                continue

            value = int(tx["input"][74:], 16)
            token = True

        result.append({
            "contract": contract.lower(),
            "receiver": receiver.lower(),
            "sender": sender.lower(),
            "txid": txid.lower(),
            "gasprice": gasprice,
            "gasused": gasused,
            "value": value,
            "token": token,
            "index": index,
            "data": data
        })

    return result

@orm.db_session
def sync_index():
    log_message("Syncing block index")

    w3 = Web3(HTTPProvider(config.endpoint))

    if config.testnet:
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    for contract in config.contracts:
        if not Contract.get(address=contract["address"]):
            Contract(**contract)

    latest = Block.select().order_by(
        orm.desc(Block.height)
    ).first()

    if not latest:
        latest = Block(**{
            "blockhash": config.start_hash,
            "height": config.start_height
        })

    current_height = w3.eth.blockNumber

    log_message(f"Current height {current_height}, db height {latest.height}")

    if latest.blockhash != w3.eth.getBlock(latest.height)["hash"].hex():
        log_message(f"Found reorg at height {latest.height}")

        reorg_block = latest
        latest = Block.get(height=reorg_block.height - 1)

        if not latest or latest.height == config.start_height:
            log_message("Reorg before start block, aborting")
            return None

        reorg_block.delete()
        orm.commit()

    for height in range(latest.height + 1, current_height + 1):
        data = w3.eth.getBlock(height)
        created = datetime.fromtimestamp(data["timestamp"])
        block = Block(**{
            "blockhash": data["hash"].hex(),
            "created": created,
            "height": height
        })

        txs = process_transactions(w3, height)
        log_message(f"New block #{block.height}, {block.blockhash}, {len(txs)} tx")

        for tx in txs:
            contract = Contract.get(address=tx["contract"])
            token = tx["token"]

            if token and not contract:
                continue

            decimals = DECIMALS if not token else contract.decimals

            if not (receiver := Address.get(address=tx["receiver"])):
                receiver = Address(**{"address": tx["receiver"]})

            if not (sender := Address.get(address=tx["sender"])):
                sender = Address(**{"address": tx["sender"]})

            Transaction(**{
                "value": amount(tx["value"], decimals),
                "contract": contract,
                "receiver": receiver,
                "index": tx["index"],
                "txid": tx["txid"],
                "data": tx["data"],
                "sender": sender,
                "token": token,
                "block": block
            })

        orm.commit()
