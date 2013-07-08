#!/bin/sh
DB_NAME=$1
SQL=$2
TMP_DAT=$3
mysql -uroot -B $DB_NAME < $SQL |sed '1d' |python main.py -c 10.41 -z -o $TMP_DAT
