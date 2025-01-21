# paperless_asnlist

A simple script to pull a CSV with paperless ASNs to store in a backup, not written for efficiency.

## Usage

Setup:
```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install requests

cp paperless.cfg.ini paperless.cfg
$EDITOR paperless.cfg
```

Usage:
```bash
./paperless_asnlist.py
```