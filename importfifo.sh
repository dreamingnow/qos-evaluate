#!/bin/bash
pipe=`realpath $1`
DB_NAME=$3
mysql -uroot --show-warnings --local-infile -e "LOAD DATA LOCAL INFILE '$pipe' INTO TABLE $2 FIELDS TERMINATED BY '\\t' LINES TERMINATED BY '\\n'" $DB_NAME
