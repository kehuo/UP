DROP TABLE IF EXISTS `raw_overview`;
CREATE TABLE `raw_overview` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tmj_daily_trans_report_2.cnt` varchar(256) NOT NULL COMMENT "小微主扫/快速收款码",
  `tmj_daily_trans_report_2.index` int(11) NOT NULL COMMENT "当日新增用户",
  `tmj_daily_trans_report_2.part_dt` int(11) NOT NULL COMMENT "当日活跃用户",
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` int(11) NOT NULL DEFAULT 0,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_uni` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `raw_transaction_cnt_by_day`;
CREATE TABLE `raw_transaction_cnt_by_day` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index` varchar(256) NOT NULL COMMENT "小微主扫/快速收款码",
  `cnt_today` int(11) NOT NULL COMMENT "当日新增用户",
  `cnt_yesterday` int(11) NOT NULL COMMENT "当日活跃用户",
  `ratio` float(20, 18) NOT NULL COMMENT "当日活跃用户",
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` int(11) NOT NULL DEFAULT 0,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_uni` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `raw_qr_transaction_cnt_by_scene`;
CREATE TABLE `raw_qr_transaction_cnt_by_scene` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `scene` varchar(256) NOT NULL COMMENT "小微主扫/快速收款码",
  `cnt_today` int(11) NOT NULL COMMENT "当日新增用户",
  `cnt_yesterday` int(11) NOT NULL COMMENT "当日活跃用户",
  `ratio` float(20, 18) NOT NULL COMMENT "当日活跃用户",
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` int(11) NOT NULL DEFAULT 0,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_uni` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `raw_qr_transaction_by_merchant`;
CREATE TABLE `raw_qr_transaction_by_merchant` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `branch` varchar(256) NOT NULL COMMENT "小微主扫/快速收款码",
  `city` int(11) NOT NULL COMMENT "当日新增用户",
  `mchnt_cd` int(11) NOT NULL COMMENT "当日活跃用户",
  `mchnt_cd` int(11) NOT NULL COMMENT "当日活跃用户",
  `mchnt_cd` int(11) NOT NULL COMMENT "当日活跃用户",
  `mchnt_cd` int(11) NOT NULL COMMENT "当日活跃用户",
  `mchnt_cd` int(11) NOT NULL COMMENT "当日活跃用户",
  `mchnt_cd` int(11) NOT NULL COMMENT "当日活跃用户",
  `ratio` float(20, 18) NOT NULL COMMENT "当日活跃用户",
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` int(11) NOT NULL DEFAULT 0,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_uni` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;