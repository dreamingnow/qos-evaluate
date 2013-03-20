Usage
======================================

Preprocessing
-------------
Raw segment log data files contain 12 columns for a single video chunk.

1. epoch finished
2. transfer time
3. IP (32-bit int)
4. port
5. file size
6. channel
7. HTTP status code
9. bitrate
10. connection sequence number
11. server name
12. user agent

Since iOS devices has unified protocol (same buffer size), the data file should be first filtered to keep only iOS records.  Then it needs to be ordered by sessions and time.
It should be ordered by server name (11),  connection sequence (10), and time (1).  The script `filsort.sh` can do this for us.  Change path of raw data in the script before use.

`./filsort.sh <start_date> <end_date> <server_name>`

It will produce preprocessed data file `dat_<server_name>_<start_date>_<end_date>.gz`.

Estimate QoE of sessions
------------------------

`python qoeest.py <preprocessed_dat_file> > <output_file>`

The format of preprocessed dat file produced by `filsort.sh` should be a sorted segment download log, which has the same 12 columns as the original seg file produced by nginx.

`qoeest.py` outputs the result to `stdout`.  So we can redirect output to a file.  `runQoeest.sh` will output the result to a gzipped file with prefix `qoe_`.

`./runQoeest.sh <preprocessed_dat_file>`

The file `batch.sh` automates the processing and move the output file to specified directory.







