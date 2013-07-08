/*
SQLyog Ultimate v10.42 
MySQL - 5.1.66-0+squeeze1 : Database - mobtv_qoe_20130527
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
/*Table structure for table `est_slot_seg` */

DROP TABLE IF EXISTS `est_slot_seg`;

CREATE TABLE `est_slot_seg` (
  `os` enum('an','ios','all') NOT NULL,
  `time_slot` int(10) unsigned NOT NULL,
  `est_seg` float NOT NULL,
  PRIMARY KEY (`os`,`time_slot`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*Table structure for table `exclude_log` */

DROP TABLE IF EXISTS `exclude_log`;

CREATE TABLE `exclude_log` (
  `serv_name` enum('68-168-103-139.phx.dedicated.codero.com','dop-tel-fj-pt-001','dop-tel-fj-pt-002','dop-tel-gd-st-003','dop-tel-gd-st-004','dop-tel-gd-zh-002','dop-tel-gd-zh-003','dop-tel-hb-xf-002','dop-tel-hn-sy-003','dop-tel-hn-sy-004','dop-tel-js-nt-001','dop-tel-js-nt-002','dop-tel-jx-nc-002','dop-tel-jx-nc-003','dop-tel-sc-ms-001','dop-tel-sc-ms-002','dop-tel-zj-nb-002','dop-tel-zj-nb-003','dop-uni-he-ly-001','dop-uni-he-ly-002','dop-uni-nm-tl-002','dop-uni-nm-tl-003','dop-uni-sd-zb-001','dop-uni-sd-zb-002','dop-uni-sx-ty-003','dop-uni-sx-ty-004') DEFAULT NULL,
  `conn_seq` int(10) unsigned DEFAULT NULL,
  `arr_time` double DEFAULT NULL,
  KEY `idx_sess` (`serv_name`,`conn_seq`),
  KEY `idx_time` (`arr_time`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*Table structure for table `seg_log` */

DROP TABLE IF EXISTS `seg_log`;

CREATE TABLE `seg_log` (
  `arr_time` double DEFAULT NULL,
  `down_time` float DEFAULT NULL,
  `ip_num` int(10) unsigned DEFAULT NULL,
  `port` smallint(5) unsigned DEFAULT NULL,
  `file_size` int(10) unsigned DEFAULT NULL,
  `channel` varchar(16) DEFAULT NULL,
  `http_code` smallint(5) unsigned DEFAULT NULL,
  `seg_seq` int(10) unsigned DEFAULT NULL,
  `bitrate` enum('64k','128k','256k','512k','900k') DEFAULT NULL,
  `conn_seq` int(10) unsigned DEFAULT NULL,
  `serv_name` enum('68-168-103-139.phx.dedicated.codero.com','dop-tel-fj-pt-001','dop-tel-fj-pt-002','dop-tel-gd-st-003','dop-tel-gd-st-004','dop-tel-gd-zh-002','dop-tel-gd-zh-003','dop-tel-hb-xf-002','dop-tel-hn-sy-003','dop-tel-hn-sy-004','dop-tel-js-nt-001','dop-tel-js-nt-002','dop-tel-jx-nc-002','dop-tel-jx-nc-003','dop-tel-sc-ms-001','dop-tel-sc-ms-002','dop-tel-zj-nb-002','dop-tel-zj-nb-003','dop-uni-he-ly-001','dop-uni-he-ly-002','dop-uni-nm-tl-002','dop-uni-nm-tl-003','dop-uni-sd-zb-001','dop-uni-sd-zb-002','dop-uni-sx-ty-003','dop-uni-sx-ty-004') DEFAULT NULL,
  `os` enum('an','ios-small','ios-large') DEFAULT NULL,
  KEY `idx_arr` (`arr_time`),
  KEY `idx_sess` (`serv_name`,`conn_seq`),
  KEY `idx_down` (`down_time`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*Table structure for table `sess_qoe` */

DROP TABLE IF EXISTS `sess_qoe`;

CREATE TABLE `sess_qoe` (
  `serv_name` enum('68-168-103-139.phx.dedicated.codero.com','dop-tel-fj-pt-001','dop-tel-fj-pt-002','dop-tel-gd-st-003','dop-tel-gd-st-004','dop-tel-gd-zh-002','dop-tel-gd-zh-003','dop-tel-hb-xf-002','dop-tel-hn-sy-003','dop-tel-hn-sy-004','dop-tel-js-nt-001','dop-tel-js-nt-002','dop-tel-jx-nc-002','dop-tel-jx-nc-003','dop-tel-sc-ms-001','dop-tel-sc-ms-002','dop-tel-zj-nb-002','dop-tel-zj-nb-003','dop-uni-he-ly-001','dop-uni-he-ly-002','dop-uni-nm-tl-002','dop-uni-nm-tl-003','dop-uni-sd-zb-001','dop-uni-sd-zb-002','dop-uni-sx-ty-003','dop-uni-sx-ty-004') NOT NULL DEFAULT '68-168-103-139.phx.dedicated.codero.com',
  `conn_seq` int(10) unsigned NOT NULL,
  `channel` varchar(16) DEFAULT NULL,
  `bitrate` enum('64k','128k','256k','512k','900k') DEFAULT NULL,
  `ip_num` int(10) unsigned DEFAULT NULL,
  `os` enum('an','ios-small','ios-large') DEFAULT NULL,
  `epoch_start` double DEFAULT NULL,
  `epoch_end` double DEFAULT NULL,
  `total_seg` int(10) unsigned DEFAULT NULL,
  `filtered_seg` int(10) unsigned DEFAULT NULL COMMENT 'exclude additional segments while buffering',
  `avg_down_time` float DEFAULT NULL,
  `num_stuck` int(10) unsigned DEFAULT NULL,
  `buf_time` float DEFAULT NULL,
  `play_time` float DEFAULT NULL,
  `last_stuck` double DEFAULT NULL,
  `last_resume` double DEFAULT NULL,
  PRIMARY KEY (`serv_name`,`conn_seq`),
  KEY `idx_start` (`epoch_start`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*Table structure for table `state_log` */

DROP TABLE IF EXISTS `state_log`;

CREATE TABLE `state_log` (
  `serv_name` enum('68-168-103-139.phx.dedicated.codero.com','dop-tel-fj-pt-001','dop-tel-fj-pt-002','dop-tel-gd-st-003','dop-tel-gd-st-004','dop-tel-gd-zh-002','dop-tel-gd-zh-003','dop-tel-hb-xf-002','dop-tel-hn-sy-003','dop-tel-hn-sy-004','dop-tel-js-nt-001','dop-tel-js-nt-002','dop-tel-jx-nc-002','dop-tel-jx-nc-003','dop-tel-sc-ms-001','dop-tel-sc-ms-002','dop-tel-zj-nb-002','dop-tel-zj-nb-003','dop-uni-he-ly-001','dop-uni-he-ly-002','dop-uni-nm-tl-002','dop-uni-nm-tl-003','dop-uni-sd-zb-001','dop-uni-sd-zb-002','dop-uni-sx-ty-003','dop-uni-sx-ty-004') DEFAULT NULL,
  `conn_seq` int(10) unsigned DEFAULT NULL,
  `state` enum('buf','play','stop') DEFAULT NULL,
  `transition_epoch` double DEFAULT NULL,
  `stuck_seq` int(10) unsigned DEFAULT NULL,
  KEY `idx_sess` (`serv_name`,`conn_seq`),
  KEY `idx_time` (`transition_epoch`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
