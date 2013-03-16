#!/bin/bash
#set -x
DATAPATH='/home/dopool/serv_trace/data/'
SCRIPTPATH=`dirname "$0"`
if (( $# < 2 )) ; then
    echo 'usage: filsort.sh <start_date> <end_date>'
    exit 1
fi


# FILENAME=`basename "$DATAFILE"`
# echo Processing $FILENAME
# ### Note: only keep iOS clients

#SERVER='dop-uni-sx-ty-003'
#SERVER='dop-tel-zj-nb-003'
SERVER=$3
STARTDATE=`date -d "$1" +%Y%m%d`
CURDATE=`date -d "$1" +%Y%m%d`
ENDDATE=`date -d "$2" +%Y%m%d`
cat /dev/null > filter.tmp
while [[ "$CURDATE" < "$ENDDATE" ]]
do
    echo Processing $CURDATE
    MONTHSTR=`date -d "$CURDATE" +%Y%m`
    DATAFILE="$DATAPATH"/access.log."$1".$SERVER.seg.gz
    zcat $DATAFILE |awk '$12 ~ /Apple/ {print $0;}' >> filter.tmp

    CURDATE=`date -d "$CURDATE +1 days" +%Y%m%d`
done
echo Sorting...
sort -t\t -k11 -k10n -k1n filter.tmp | gzip > "dat_${SERVER}_${STARTDATE}_${ENDDATE}.gz"
