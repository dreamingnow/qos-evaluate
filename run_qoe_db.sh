#!/bin/sh
DB_NAME=$1
TMP_DAT=$2
mysql -uroot -B $DB_NAME < sql/seg_all.sql |sed '1d' |python main.py -c 10.41 -z -o $TMP_DAT
