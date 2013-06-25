#!/usr/bin/env python
#coding:utf-8
# Author:  Howard --<>
# Purpose: estimate qoe from segment logs
# Created: 2013-03-16

import fileinput
import csv
import sys
import optparse
import gzip
import time


# status constant
S_BUF = 0
S_PLAY = 1


# parameters
BUF_THRES = 3
#SEGLEN = 10.41
SEGLEN = 10
# whether distinguish pause: True = DO NOT check
NOT_CHECK_PAUSE = True


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
    yield [0] * 2 + [None] * 10


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
    parser.add_option('-m', '--probe-mode', action='store_true',
                      dest='probe_mode', default=False,
                      help='Probe mode')
    (options, args) = parser.parse_args()
    if len(args) == 0:
        parser.error('Input file needed.')

    NOT_CHECK_PAUSE = options.chkpause
    SEGLEN = options.seglen
    BUF_THRES = options.bufthres
    is_probe = options.probe_mode
    if options.output_filename is None:
        outfile = sys.stdout
    else:
        if options.gzip:
            outfile = gzip.open(options.output_filename, 'wb')
        else:
            outfile = open(options.output_filename, 'wb')
        desc_file = open(options.output_filename + '.desc', 'wb')
        desc_file.write('not_check_pause=%s\n' % NOT_CHECK_PAUSE)
        desc_file.write('segment_length=%.2f\n' % SEGLEN)
        desc_file.write('buffer_threshold=%d\n' % BUF_THRES)
        desc_file.close()

    infile = fileinput.FileInput(files=args, openhook=fileinput.hook_compressed)

    tos = time.time()
    sys.stderr.write('[%s] Start: \n' % (time.asctime(), ))
    sys.stderr.write('not_check_pause: %s\n' % NOT_CHECK_PAUSE)
    sys.stderr.write('segment_length: %.2f\n' % SEGLEN)
    sys.stderr.write('buffer_threshold: %d\n' % BUF_THRES)

    cur_sess = None
    # session info
    sess_info = []
    # session start epoch
    #epoch_sess_start = 0
    # length of buffered video
    len_buffered = 0
    # length of freezing
    len_freezing = 0
    # length of time used for playback
    len_playback = 0
    # number of stuck
    num_stuck = 0
    # list of segment download time
    seg_down_time = []
    # number of segment in a session
    num_seg = 0
    # number of segment in a session, EXCLUDING buffering chunks
    num_seg_play = 0
    # working status of the client, can be: S_BUF / S_PLAY
    status = S_BUF
    # time cursor, pointing to the last epoch processed
    epoch_processed = 0
    #last_request = 0
    is_init_buf = True
    is_first = True
    wr = csv.writer(outfile, delimiter='\t')
    for line in fileReader(infile):
        # session identifier: server, conn_num
        s = line[10], line[9]
        # epoch of segment arrival
        t = line[0]
        # segment download time
        d = line[1]
        # request time
        r = t - d
        if s != cur_sess:
            # Jump to new session
            if cur_sess is not None and not is_probe:
                # output result of last session
                num_seg = len(seg_down_time)
                wr.writerow(list(cur_sess) + sess_info +
                            [epoch_processed, num_seg, num_seg_play,
                             sum(seg_down_time) / num_seg, num_stuck, len_freezing, len_playback])
            # initialize the new session
            cur_sess = s
            sess_info = [line[5], line[8], line[2], r]
            status = S_BUF
            is_init_buf = True
            # for the new session, set time cursor to the epoch of requesting
            # the first chunk, the beginning of the whole session
            epoch_processed = r
            len_buffered = 0
            seg_down_time = []
            len_freezing = 0
            len_playback = 0
            num_stuck = 0
            num_seg_play = 0

        if status == S_PLAY:
            len_buffered -= t - epoch_processed
            # playback consumption of buffer
            if len_buffered < 0:
                if NOT_CHECK_PAUSE or d > SEGLEN or r - epoch_processed < 0.5 * SEGLEN:
                    # check whether caused by download timeout
                    # the user may also pause the video by himself
                    num_stuck += 1
                len_playback += t - epoch_processed - (-len_buffered)
                # set epoch_processed to when the buffer depletes
                epoch_processed = t - (-len_buffered)
                status = S_BUF
                is_first = True
                len_buffered = 0
            else:
                len_playback += t - epoch_processed
            num_seg_play += 1

        len_buffered += SEGLEN
        if status == S_BUF:
            #len_freezing += t - epoch_processed
            if not is_init_buf:
                if is_first:
                    len_freezing += min(d, t - epoch_processed)
                    is_first = False
            if len_buffered >= SEGLEN * BUF_THRES:
                status = S_PLAY
                is_init_buf = False

        if is_probe and t != 0:
            wr.writerow([num_stuck, len_buffered, t - d] + line[0:2] + line[5:11])
        seg_down_time.append(d)
        epoch_processed = t
        #last_request = r

    toe = time.time()
    sys.stderr.write('[%s] Done: %.3fs.\n' % (time.asctime(), toe - tos))

if __name__ == '__main__':
    main()
