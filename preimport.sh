#!/bin/bash
#### Import $1 into db $2 through pipe $3
pipe=`realpath $3`
db_name=$2
echo Import through named pipe $pipe
zcat $1 | awk 'BEGIN{FS=OFS="\t"} {if ($12 ~ /Apple/) {if ($12 ~ /iPad/) $12="ios-large"; else $12="ios-small";} else $12="an"; print;}' >$3&
mysql -uroot --show-warnings --local-infile -e "LOAD DATA LOCAL INFILE '$pipe' INTO TABLE seg_log FIELDS TERMINATED BY '\\t' LINES TERMINATED BY '\\n'" $db_name

