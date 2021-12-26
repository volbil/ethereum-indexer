from ..models import Transaction
from ..models import Address
from flask import Blueprint
from pony import orm

blueprint = Blueprint("v1", __name__, url_prefix="/v1")

@blueprint.route("/history/<string:address>", methods=["GET"])
@orm.db_session
def history(address):
    result = {"error": None, "data": []}

    if (address := Address.get(address=address.lower())):
        transactions = Transaction.select(
            lambda t: t.sender == address or t.receiver == address
        )

    return result

@blueprint.route("/transaction/<string:txid>", methods=["GET"])
@orm.db_session
def transaction(txid):
    result = {"error": None, "data": {}}

    if (transaction := Transaction.get(txid=txid.lower())):
        contract = None if not transaction.contract else {
            "decimals": transaction.contract.decimals,
            "address": transaction.contract.address,
            "ticker": transaction.contract.ticker,
            "name": transaction.contract.name
        }

        return {
            "receiver": transaction.receiver.address,
            "sender": transaction.sender.address,
            "value": float(transaction.value),
            "index": transaction.index,
            "token": transaction.token,
            "data": transaction.data,
            "txid": transaction.txid,
            "contract": contract,
            "block": {
                "created": int(transaction.block.created.timestamp()),
                "blockhash": transaction.block.blockhash,
                "height": transaction.block.height
            }
        }

    return result
