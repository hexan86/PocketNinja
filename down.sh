#!/bin/bash

#d=$(date'+%d%m%Y_%H%M');
DATE_BIN=$(command -v date)
d=`${DATE_BIN} +%d-%m-%y_%H.%M.%S`

sudo pm3 -c auto >> /home/kali/pm3_scan_$d.txt

DATA_BIN=$(command -v cat)

c=`${DATA_BIN} /home/kali/pm3_scan_*.txt | grep Valid`
if [ -z "$c" ]
then
      echo "\Nothing to show"
else
      t1="$c$d"
      printf "\nt $t1\n exit()" | rainbowstream
fi

sleep 20

h=`${DATA_BIN} /home/kali/pm3_scan_*.txt | grep Hint`
if [ -z "$h" ]
then
      echo "\Nothing to show"
else
      t2="$h$d"
      printf "\nt $t2\n exit()" | rainbowstream
fi


mv /home/kali/pm3_scan*.txt /home/kali/RFID/NinjaArchive

exit 0
