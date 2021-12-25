from datetime import datetime
from decimal import Decimal
from pony import orm
import config

db = orm.Database(**config.db)

class Block(db.Entity):
    _table_ = "service_blocks"

    created = orm.Optional(datetime)
    blockhash = orm.Required(str)
    height = orm.Required(int)

    transactions = orm.Set("Transaction")

class Contract(db.Entity):
    _table_ = "service_contracts"

    decimals = orm.Required(int)
    address = orm.Required(str)
    ticker = orm.Required(str)
    name = orm.Required(str)

    transactions = orm.Set("Transaction")

class Address(db.Entity):
    _table_ = "service_addresses"

    address = orm.Required(str)

    transactions_receiver = orm.Set("Transaction", reverse="receiver")
    transactions_sender = orm.Set("Transaction", reverse="sender")

class Transaction(db.Entity):
    _table_ = "service_transactions"

    value = orm.Required(Decimal, precision=20, scale=18)
    token = orm.Required(bool, default=False)
    txid = orm.Required(str, index=True)
    contract = orm.Optional("Contract")
    receiver = orm.Required("Address")
    sender = orm.Required("Address")
    block = orm.Required("Block")
    index = orm.Required(int)
    data = orm.Required(str)


db.generate_mapping(create_tables=True)