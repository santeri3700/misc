#!/bin/bash
# ./cs02_imei_editor [OPTION] [FILE] [[NEWIMEI]]
# OPTIONS:
# -p, --print    Prints the IMEI and other info.
# -e, --edit     Replaces IMEI with [NEWIMEI].
# -h, --help     Prints the help message.
#
# [FILE] is the CAL image (mmcblk0p1) dumped from the phone.
# [NEWIMEI] must be a correct IMEI. This is NOT checked so be careful!
#
# https://en.wikipedia.org/wiki/International_Mobile_Equipment_Identity
#
# I take NO responsibility of anything done with this tool!
# This tool is made to fix bricked SM-G350 using another SM-G350's CAL partition.
# It is illegal to change IMEI in some coutries but this can also be an exceptions
# because our intention is to keep the old IMEI.

# Type Allocation Code list for SM-G350 (INCOMPLETE!)
# - 35849505
# - 35752806
# - 35505906

cs02tac=35849505 # This is one of many TAC's for SM-G350. _Change this if needed!_

# Get offset
if [ $2 ] && [ -f $2 ]; then
    offsetdec=$(grep -oba $cs02tac $2 | sed 's/:.*//')
    offsethex=$(printf '%x' $offsetdec)
    imeioffset=0x$offsethex
    dumpimei=$(hexdump -e "15 \"%_p\" \"\\n\"" -s $imeioffset -n 15 $2)
    imeitac=$(echo $dumpimei | head -c 8)
    imeisn=$(echo $dumpimei | tail -c 8 | head -c 6)
    imeicd=$(echo $dumpimei | tail -c 2)
fi

echo "SM-G350 [cs02] IMEI extractor and editor"
echo "---------------"

case $1 in
-p|--print)
    if [ $imeitac != $cs02tac ]; then
	echo "This is NOT a valid SM-G350 [cs02] CAL image! Edit TAC from the script?"
	exit 1
    fi
    echo "File: $2"
    echo "Offset: $imeioffset"
    echo "IMEI: \"$dumpimei\""
    echo "---------------"
    echo "TAC: $imeitac"
    echo "SN: $imeisn"
    echo "CD: $imeicd"
    echo "---------------"
    ;;
-e|--edit)
    echo "# EDITING! THIS IS UNTESTED AND DANGEROUS! #"
    echo "File: $2"
    echo "IMEI: \"$dumpimei\""
    echo "---------------"
    if [ ${#3} == 15 ]; then
    	echo "NEW IMEI: \"$3\""
    else
	echo "Error: Invalid new IMEI length!"
	exit 1
    fi
    cp $2 $2.bak
    sed -i "s/$dumpimei/$3/g" "$2"
    echo "Changed saved to $2. VERIFY THE IMEI BEFORE FLASHING! USE THIS TOOL TO CHECK THE NEW FILE BEFORE FLASHING! THIS FUNCTION IS UNTESTED!"
    echo "*** The original file is named $2.bak ***"
    echo "Done!"
    ;;
*)
    echo "
./cs02_imei_editor [OPTION] [FILE] [[NEWIMEI]]
OPTIONS:
-p, --print    Prints the IMEI and other info.
-e, --edit     Replaces IMEI with [NEWIMEI].
-h, --help     Prints the help message.

[FILE] is the CAL image (mmcblk0p1) dumped from the phone.
[NEWIMEI] must be a correct IMEI. This is NOT checked so be careful!
"
    ;;
esac
