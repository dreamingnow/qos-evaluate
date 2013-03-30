#!/usr/bin/env python
#coding:utf-8
# Author:  Yuheng Li --<liyuheng07@gmail.com>
# Purpose:
# Created: 2013/3/27

import MySQLdb
import MySQLdb.cursors
import csv
import sys
import collections
import optparse


def dbReader(conn, sql):
    """mysql db reader"""
    c = conn.cursor()
    c.execute(sql)
    while True:
        rec = c.fetchone()
        if rec is not None:
            yield rec
        else:
            break
    c.close()
    conn.close()


def main():
    """main
    :returns: @todo

    """
    parser = optparse.OptionParser()
    parser.set_usage('%prog [options] FILES')
    parser.add_option('-o', '--output', action='store',
                      type='string', dest='output_filename',
                      help='Output file')
    parser.add_option('-t', '--type', action='store',
                      type='string', dest='os_type', default='all',
                      help='OS type: all/an/ios')
    parser.add_option('-c', '--chunk-length', action='store',
                      type='float', dest='seglen', default=10,
                      help='Segment length')
    parser.add_option('-i', '--interval', action='store',
                      type='int', dest='interval', default=60,
                      help='Time slot length')
    (options, args) = parser.parse_args()
    conn = MySQLdb.connect(host='dreamseat.3322.org', user='qoe',
                           passwd='qoe@dreamseat', db='mobtv_qoe',
                           cursorclass=MySQLdb.cursors.DictCursor)
    seglen = options.seglen
    interval = options.interval

    if options.output_filename is None:
        outfile = sys.stdout
    else:
        outfile = open(options.output_filename, 'wb')

    sql = '''
SELECT
  `serv_name`,
  `conn_seq`,
  `channel`,
  `bitrate`,
  `ip_num`,
  `os`,
  `epoch_start`,
  `epoch_end`,
  `total_seg`,
  `filtered_seg`,
  `avg_down_time`,
  `num_stuck`,
  `buf_time`,
  `play_time`
FROM `mobtv_qoe`.`sess_qoe`
WHERE `avg_down_time` > 0 AND `filtered_seg` > 0
'''
    if options.os_type == 'an' or options.os_type == 'ios':
        sql += ''' AND `os` = "%s";''' % (options.os_type)
    else:
        sql += ';'
    timeslots = collections.defaultdict(float)
    for line in dbReader(conn, sql):
        # session
        #s = line[0], line[1]
        # start, end time
        t_start = line['epoch_start']
        t_end = line['epoch_end']
        ts_start = int(t_start - t_start % interval)
        ts_end = int(t_end - t_end % interval)
        a = line['avg_down_time']
        for t in range(ts_start, ts_end + interval, interval):
            rho = seglen / a
            pi0 = 1.0 * line['num_stuck'] / line['filtered_seg']
            r = rho / (rho + pi0)
            timeslots[t] += (min(t + interval, t_end) - max(t, t_start)) * r / seglen

    wr = csv.writer(outfile, delimiter='\t', lineterminator='\n')
    for k in sorted(timeslots.keys()):
        wr.writerow([k, timeslots[k]])


if __name__ == '__main__':
    main()
