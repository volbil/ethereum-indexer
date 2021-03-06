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

secret = "Lorem ipsum dor sit amet"
host = "0.0.0.0"
debug = True
port = 4321

db = {
    "provider": "sqlite",
    "filename": "../local.db",
    "create_db": True
}
```

## Systemd

Sync serivce `/etc/systemd/system/sync.service`:

```
[Unit]
Description=Indexer sync service
After=multi-user.target

[Service]
Type=idle
ExecStart=/home/user/indexer/venv/bin/python3 /home/user/indexer/sync.py
WorkingDirectory=/home/user/indexer
User=user

[Install]
WantedBy=multi-user.target
```

API service `/etc/systemd/system/api.service`:

```
[Unit]
Description=Gunicorn instance to serve indexer API
After=network.target

[Service]
User=user
Group=www-data
WorkingDirectory=/home/user/indexer
Environment="PATH=/home/user/indexer/venv/bin"
ExecStart=/home/user/indexer/venv/bin/gunicorn app:app --worker-class gevent -w 1 --bind 0.0.0.0:4321 --reload

[Install]
WantedBy=multi-user.target
```

## Nginx

Nginx config `/etc/nginx/sites-available/example.com.conf`:

```
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://localhost:4321;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```
