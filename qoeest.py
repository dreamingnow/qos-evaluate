#!/usr/bin/env python
#coding:utf-8
# Author:  Howard --<>
# Purpose: estimate qoe from segment logs
# Created: 2013-03-16

import fileinput
import csv
import sys

SEGLEN = 10
S_BUF = 0
S_PLAY = 1
BUF_THRES = 3


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
    yield [None] * 12


def main():
    """main
    """
    outfile = sys.stdout
    cur_sess = None
    # session info
    sess_info = []
    # session start epoch
    #epoch_sess_start = 0
    # length of buffered video
    len_buffered = 0
    # length of downloaded video
    #len_downloaded = 0
    # length of freezing
    len_freezing = 0
    # length of time elapsed
    #len_elapsed = 0
    # number of stuck
    num_stuck = 0
    # list of segment download time
    seg_down_time = []
    # number of segment in a session
    num_seg = 0
    # working status of the client, can be: S_BUF / S_PLAY
    status = S_BUF
    last_arrival = 0
    wr = csv.writer(outfile, delimiter='\t')
    for line in fileReader(fileinput.FileInput(openhook=fileinput.hook_compressed)):
        # session identifier: server, conn_num
        s = line[10], line[9]
        # epoch of segment arrival
        t = line[0]
        # segment download time
        d = line[1]
        if s != cur_sess:
            # Jump to new session
            if cur_sess is not None:
                # output result of last session
                num_seg = len(seg_down_time)
                wr.writerow(list(cur_sess) + sess_info +
                            [num_seg, sum(seg_down_time) / num_seg, num_stuck])
            # initialize new session
            cur_sess = s
            sess_info = [line[5], line[8], line[2], line[11]]
            status = S_BUF
            last_arrival = t
            #epoch_sess_start = t
            len_buffered = SEGLEN
            seg_down_time = [d]
            #len_downloaded = SEGLEN
            len_freezing = 0
            num_stuck = 0
        else:
            #len_downloaded += SEGLEN
            if status == S_PLAY:
                len_buffered -= t - last_arrival
                # playback consumption of buffer
                if len_buffered < 0:
                    num_stuck += 1
                    len_freezing += -len_buffered
                    status = S_BUF
                    len_buffered = 0
            else:
                # status: S_BUF
                if len_buffered >= SEGLEN * BUF_THRES:
                    status = S_PLAY

            len_buffered += SEGLEN
            seg_down_time.append(d)
            last_arrival = t


if __name__ == '__main__':
    main()
