from ..models import Transaction, Address
from webargs.flaskparser import use_args
from .args import history_args
from flask import Blueprint
from pony import orm

blueprint = Blueprint("v1", __name__, url_prefix="/v1")

@blueprint.route("/history/<string:address>", methods=["GET"])
@use_args(history_args, location="query")
@orm.db_session
def history(args, address):
    result = {"error": None, "data": []}

    if address := Address.get(address=address.lower()):
        transactions = Transaction.select(
            lambda t: t.sender == address or t.receiver == address
        ).order_by(
            orm.desc(Transaction.id)
        ).page(
            args["page"], 100
        )

        for transaction in transactions:
            result["data"].append(transaction.display)

    return result

@blueprint.route("/transaction/<string:txid>", methods=["GET"])
@orm.db_session
def transaction(txid):
    result = {"error": None, "data": {}}

    if transaction := Transaction.get(txid=txid.lower()):
        result["data"] = transaction.display

    return result
