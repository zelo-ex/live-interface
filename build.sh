#/bin/sh

uv sync
uv run pyinstaller -F -w -n "live-interface" ./src/main.py
