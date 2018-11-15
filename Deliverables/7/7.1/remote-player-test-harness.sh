#!/usr/bin/env bash

python3 player_driver.py & sleep 1 && python3 main.py
# sleep 10
# lsof -n -i4TCP:9999 | grep LISTEN | awk '{ print $2 }' | xargs kill