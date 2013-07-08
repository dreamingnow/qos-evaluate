#!/bin/sh
### automatic processing of data
### Usage: ./batch.sh <file_list> <db_name>
PIPE=/tmp/tmp_pipe
TMP_DAT=temp.gz
#DB_NAME=mobtv_qoe_new
DB_NAME=$2
#SEG_FILE_LIST=files.lst
SEG_FILE_LIST=$1
SQL="sql/seg_all.sql"

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
./run_qoe_db.sh $DB_NAME $SQL $TMP_DAT
echo Save session data to DB
./importgztab.sh $TMP_DAT $DB_NAME sess_qoe $PIPE
echo Save state transitions to DB
./importgztab.sh st_$TMP_DAT $DB_NAME state_log $PIPE
echo Save excluding segment log to DB
./importgztab.sh ex_$TMP_DAT $DB_NAME exclude_log $PIPE
echo Clean
rm $PIPE $TMP_DAT st_$TMP_DAT
echo Finish \\a

