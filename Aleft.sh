#!/bin/bash

DATE_BIN=$(command -v date)
d=`${DATE_BIN} +%d-%m-%y_%H.%M.%S`

host=192.168.0.0/24

sudo nmap -e wlan0 -oN /home/kali/nmap_scans/LANs/192.168.0.x/fast-lan_$d -sS -F -T5 $host

exit 0
