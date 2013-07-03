#!/bin/sh
### automatic processing of data
PIPE=/tmp/tmp_pipe
TMP_DAT=temp.gz
DB_NAME=mobtv_qoe_new
#SEG_FILE_LIST=files.lst
SEG_FILE_LIST=$1

[ -e $PIPE ] && rm $PIPE
echo Create pipe
mkfifo $PIPE
echo Import raw data
cat "$SEG_FILE_LIST" | while read SEG_FILE
do
	echo $SEG_FILE
	./preimport.sh $SEG_FILE $DB_NAME $PIPE
done
echo Generating QoE data from raw data
./run_qoe_db.sh $DB_NAME $TMP_DAT
echo Save session data to DB
./importgztab.sh $TMP_DAT $DB_NAME sess_qoe $PIPE
echo Save stuck epochs to DB
./importgztab.sh st_$TMP_DAT $DB_NAME stuck_log $PIPE
echo Clean
rm $PIPE $TMP_DAT st_$TMP_DAT
echo Finish \\a

