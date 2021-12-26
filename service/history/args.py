from webargs import fields

history_args = {
    "page": fields.Int(missing=1, validation=lambda p: p > 0)
}
