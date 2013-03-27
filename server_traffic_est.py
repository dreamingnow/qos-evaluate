#!/usr/bin/env python
#coding:utf-8
# Author:  Yuheng Li --<liyuheng07@gmail.com>
# Purpose:
# Created: 2013/3/27

import sys
import csv
import optparse
import fileinput
import gzip
import collections


#----------------------------------------------------------------------
def fileReader(infile):
    """file reader"""
    #0. server
    #1. connection sequence
    #2. channel
    #3. bitrate
    #4. IP
    #5. start time (request time of the first chunk)
    #6. end time (finish time of the last chunk)
    #7. total segments
    #8. number of segments excluding additional segments when buffering
    #9. average segment download time
    #10. number of stuck
    #11. buffering time
    #12. playback time
    for line in csv.reader(infile, delimiter='\t'):
        line[1] = int(line[1])
        line[4] = int(line[4])
        line[5] = float(line[5])
        line[6] = float(line[6])
        line[7] = int(line[7])
        line[8] = int(line[8])
        line[9] = float(line[9])
        line[10] = int(line[10])
        line[11] = float(line[11])
        line[12] = float(line[12])
        yield line


def main():
    """main
    :returns: @todo

    """
    parser = optparse.OptionParser()
    parser.set_usage('%prog [options] FILES')
    parser.add_option('-o', '--output', action='store',
                      type='string', dest='output_filename',
                      help='Output file')
    parser.add_option('-z', '--gzip', action='store_true',
                      dest='gzip',
                      help='Gzip output file, only effective when output file is specified')
    parser.add_option('-c', '--chunk-length', action='store',
                      type='float', dest='seglen', default=10,
                      help='Segment length')
    parser.add_option('-i', '--interval', action='store',
                      type='int', dest='interval', default=60,
                      help='Time slot length')
    (options, args) = parser.parse_args()

    seglen = options.seglen
    interval = options.interval

    if options.output_filename is None:
        outfile = sys.stdout
    else:
        if options.gzip:
            outfile = gzip.open(options.output_filename, 'wb')
        else:
            outfile = open(options.output_filename, 'wb')

    if len(args) == 0:
        infile = fileinput.FileInput(files=[])
    else:
        infile = fileinput.FileInput(files=args, openhook=fileinput.hook_compressed)

    timeslots = collections.defaultdict(int)
    for line in fileReader(infile):
        # session
        #s = line[0], line[1]
        # start, end time
        t_start = line[5]
        t_end = line[6]
        ts_start = int(line[5] - line[5] % interval)
        ts_end = int(line[6] - line[6] % interval)
        a = line[9]
        for t in range(ts_start, ts_end + interval, interval):
            rho = seglen / a
            pi0 = line[10] / line[7]
            r = rho / (rho + pi0)
            timeslots[t] += (min(t + interval, t_end) - max(t, t_start)) * r / seglen

    wr = csv.writer(outfile, delimiter='\t')
    for k in sorted(timeslots.keys()):
        wr.writerow[k, timeslots[k]]


if __name__ == '__main__':
    main()
