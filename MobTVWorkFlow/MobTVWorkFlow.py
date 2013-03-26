#!/usr/bin/env python
#coding:utf-8
# Author:  Yuheng Li --<liyuheng07@gmail.com>
# Purpose: simulate the workflow of mobile TV clients
# Created: 2013/3/26


########################################################################
class MobTVWorkFlow:
    """class simulating the mobile tv workflow"""

    # status constant
    S_BUF = 0
    S_PLAY = 1

    #----------------------------------------------------------------------
    def __init__(self, chkpause, seglen, bufthres):
        """Constructor"""
        self.NOT_CHECK_PAUSE = chkpause
        self.SEGLEN = seglen
        self.BUF_THRES = bufthres
        self.cur_sess = None
        # session info
        self.sess_info = None
        # length of buffered video
        self.len_buffered = 0
        # length of freezing
        self.len_freezing = 0
        # length of time used for playback
        self.len_playback = 0
        # number of stuck
        self.num_stuck = 0
        # list of segment download time
        self.seg_down_time = []
        # number of segment in a session
        self.num_seg = 0
        # number of segment in a session, EXCLUDING buffering chunks
        self.num_seg_play = 0
        # working status of the client, can be: S_BUF / S_PLAY
        self.status = MobTVWorkFlow.S_BUF
        # time cursor, pointing to the last epoch processed
        self.epoch_processed = 0
        #last_request = 0
        self.is_init_buf = True
        self.is_first = True

    #----------------------------------------------------------------------
    def append(self, line):
        """append new record"""
        # epoch of segment arrival
        t = line[0]
        # segment download time
        d = line[1]
        # request time
        r = t - d
        if self.cur_sess is None:
            # initialize the new session
            self.cur_sess = line[10], line[9]
            self.sess_info = [line[5], line[8], line[2], r]
            self.status = MobTVWorkFlow.S_BUF
            self.is_init_buf = True
            # for the new session, set time cursor to the epoch of requesting
            # the first chunk, the beginning of the whole session
            self.epoch_processed = r
            self.len_buffered = 0
            self.seg_down_time = []
            self.len_freezing = 0
            self.len_playback = 0
            self.num_stuck = 0
            self.num_seg_play = 0

        if self.status == MobTVWorkFlow.S_PLAY:
            self.len_buffered -= t - self.epoch_processed
            # playback consumption of buffer
            if self.len_buffered < 0:
                if self.NOT_CHECK_PAUSE or d > self.SEGLEN or r - self.epoch_processed < 0.5 * self.SEGLEN:
                    # check whether caused by download timeout
                    # the user may also pause the video by himself
                    self.num_stuck += 1
                self.len_playback += t - self.epoch_processed - (-self.len_buffered)
                # set epoch_processed to when the buffer depletes
                self.epoch_processed = t - (-self.len_buffered)
                self.status = MobTVWorkFlow.S_BUF
                self.is_first = True
                self.len_buffered = 0
            else:
                self.len_playback += t - self.epoch_processed
            self.num_seg_play += 1

        self.len_buffered += self.SEGLEN
        if self.status == MobTVWorkFlow.S_BUF:
            #len_freezing += t - epoch_processed
            if not self.is_init_buf:
                if self.is_first:
                    self.len_freezing += min(d, t - self.epoch_processed)
                    self.is_first = False
            if self.len_buffered >= self.SEGLEN * self.BUF_THRES:
                self.status = MobTVWorkFlow.S_PLAY
                self.is_init_buf = False

        self.seg_down_time.append(d)
        self.epoch_processed = t
        #last_request = r

    def stat(self):
        """output results as a tab delimited line

        :returns: a list of session info
        """
        num_seg = len(self.seg_down_time)
        return list(self.cur_sess) + self.sess_info + \
               [self.epoch_processed, 
                num_seg, 
                self.num_seg_play,
                sum(self.seg_down_time) / num_seg, 
                self.num_stuck, 
                self.len_freezing, 
                self.len_playback]
