#!/bin/bash
pipe=`realpath $4`
db_name=$2
zcat $1 >$4&
mysql -uroot --show-warnings --local-infile -e "LOAD DATA LOCAL INFILE '$pipe' INTO TABLE $3 FIELDS TERMINATED BY '\\t' LINES TERMINATED BY '\\r\\n'" $db_name
