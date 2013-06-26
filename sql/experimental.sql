-- total
SELECT COUNT(*) FROM sess_qoe;
-- exlude some session
SELECT COUNT(*) FROM sess_qoe WHERE avg_down_time > 0 AND filtered_seg > 0;

SELECT * FROM sess_qoe WHERE avg_down_time = 0;

-- stucks of filtered sessions
-- 1. filtered_seg > 0: actually played
-- 2. avg_down_time > 0: exclude abnormal arrival rate
SELECT 
  serv_name,
  conn_seq,
  stuck_epoch 
FROM
  stuck_log 
  JOIN sess_qoe USING (serv_name, conn_seq) 
WHERE avg_down_time > 0 
  AND filtered_seg > 0 ;

-- total stucks
SELECT COUNT(*) FROM stuck_log;

-- MEASUREMENT: segment log of filtered sessions
SELECT 
  serv_name,
  conn_seq,
  arr_time,
  file_size,
  seg_log.bitrate 
FROM
  seg_log 
  JOIN sess_qoe USING (serv_name, conn_seq) 
WHERE avg_down_time > 0 
  AND filtered_seg > 0 ;


-- stucks of intervals
SET @step := 60;
SELECT 
  stuck_epoch - stuck_epoch % @step AS `time.slot`,
  COUNT(*) AS `num.stuck`
FROM
  stuck_log 
  JOIN sess_qoe USING (serv_name, conn_seq) 
WHERE avg_down_time > 0 
  AND filtered_seg > 0 
GROUP BY `time.slot`;

-- count seg down and traffic of time slots
SELECT 
  arr_time - arr_time % @step AS `time.slot`,
  COUNT(*) AS `num.seg`,
  COUNT(DISTINCT serv_name, conn_seq) AS `num.sess`,
  SUM(file_size) AS `traffic`
FROM
  seg_log 
  JOIN sess_qoe USING (serv_name, conn_seq) 
WHERE avg_down_time > 0 
  AND filtered_seg > 0 
GROUP BY `time.slot`;

-- select sessions
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
WHERE `avg_down_time` > 0 AND `filtered_seg` > 0;

-- get estimated segdown number of time slots
SELECT
  `time_slot` AS `time.slot`,
  `est_seg` AS `est.num.seg`
FROM `mobtv_qoe`.`est_slot_seg`
WHERE `os` = 'ios';