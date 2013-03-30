#!/usr/bin/env python
# encoding: utf-8


import fileinput
import csv
import sys
import optparse
import gzip
import time
from MobTVWorkFlow import MobTVWorkFlow


def fileReader(infile):
    """read data from tab delimitted files
    """
    #|    0 | 时间             |
    #|    1 | 下载耗时         |
    #|    2 | IP地址           |
    #|    3 | 端口             |
    #|    4 | 块大小           |
    #|    5 | 频道             |
    #|    6 | HTTP状态         |
    #|    7 | 块编号           |
    #|    8 | bitrate          |
    #|    9 | 连接序号         |
    #|   10 | 节点（服务器名） |
    #|   11 | Agent            |
    for line in csv.reader(infile, delimiter='\t'):
        line[0] = float(line[0])
        line[1] = float(line[1])
        line[2] = int(line[2])
        line[3] = int(line[3])
        line[4] = int(line[4])
        line[6] = int(line[6])
        line[7] = int(line[7])
        line[9] = int(line[9])
        yield line
    # End of the stream
    # yield [0] * 2 + [None] * 9 + ['']


def main():
    """main
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
    parser.add_option('-b', '--buffer-threshold', action='store',
                      type='int', dest='bufthres', default=3,
                      help='Buffering threshold')
    parser.add_option('-p', '--pause-check', action='store_false',
                      dest='chkpause', default=True,
                      help='Check pause')
    (options, args) = parser.parse_args()

    NOT_CHECK_PAUSE = options.chkpause
    SEGLEN = options.seglen
    BUF_THRES = options.bufthres

    if options.output_filename is None:
        outfile = sys.stdout
    else:
        if options.gzip:
            outfile = gzip.open(options.output_filename, 'wb')
            freeze_file = gzip.open('st_' + options.output_filename, 'wb')
        else:
            outfile = open(options.output_filename, 'wb')
            freeze_file = open('st_' + options.output_filename, 'wb')
        desc_file = open(options.output_filename + '.desc', 'wb')
        desc_file.write('not_check_pause=%s\n' % NOT_CHECK_PAUSE)
        desc_file.write('segment_length=%.2f\n' % SEGLEN)
        desc_file.write('buffer_threshold=%d\n' % BUF_THRES)
        desc_file.close()

    if len(args) == 0:
        infile = fileinput.FileInput(files=[])
    else:
        infile = fileinput.FileInput(files=args, openhook=fileinput.hook_compressed)

    tos = time.time()
    sys.stderr.write('[%s] Start: \n' % (time.asctime(), ))
    sys.stderr.write('not_check_pause: %s\n' % NOT_CHECK_PAUSE)
    sys.stderr.write('segment_length: %.2f\n' % SEGLEN)
    sys.stderr.write('buffer_threshold: %d\n' % BUF_THRES)

    results = {}
    for line in fileReader(infile):
        s = line[10], line[9]
        if s not in results:
            results[s] = MobTVWorkFlow(NOT_CHECK_PAUSE, SEGLEN, BUF_THRES)
        # epoch_stuck is -1 if there is no stuck
        epoch_stuck = results[s].append(line)
        if epoch_stuck > 0:
            freeze_file.write('%s\t%d\t%f\n' % (line[10], line[9], epoch_stuck))
    wr = csv.writer(outfile, delimiter='\t')
    for sess in results:
        wr.writerow(results[sess].stat())
    toe = time.time()
    sys.stderr.write('[%s] Done: %.3fs.\n' % (time.asctime(), toe - tos))

if __name__ == '__main__':
    main()
