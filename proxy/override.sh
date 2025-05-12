#!/bin/sh

set -e

pip install httpx

exec mitmdump -s /home/mitmproxy/addon.py
