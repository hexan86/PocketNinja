#/bin/bash

ifconfig wlan1 down && sudo macchanger -r wlan1 && sudo ifconfig wlan1 up

exit 0
