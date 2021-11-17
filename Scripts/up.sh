#!/bin/bash

DATE_BIN=$(command -v date)
d=`${DATE_BIN} +%d-%m-%y_%H.%M.%S`

sudo airodump-ng -w /home/kali/Captures/$d --output-format pcap --ignore-negative-one --encrypt wep wlan1

exit 0

