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

run `qoeest.py --help` to get the usage.

The format of input preprocessed dat file produced by `filsort.sh` should be a sorted segment download log, which has the same 12 columns as the original seg file produced by nginx.

The file `jobs.py` automates the processing.

Output
------

The output of the `qoeest.py` contains:

1. server
2. connection sequence
3. channel
4. bitrate
5. IP
6. start time (request time of the first chunk)
7. end time (finish time of the last chunk)
8. total segments
9. number of segments excluding additional segments when buffering
10. average segment download time
11. number of stuck
12. buffering time
13. playback time

Each line represents a session.
