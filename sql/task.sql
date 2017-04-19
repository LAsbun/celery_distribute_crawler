-- CREATE  TABLE task(
-- task VARCHAR(256) not null "任务名称",
-- auguments TEXT DEFAULT "NULL" COMMENT "任务参数 默认是NULL 无参",
-- priority int not NULL DEFAULT 0 COMMENT "优先级 0 最低",
-- updatetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT "时间戳",
-- fail int DEFAULT 0 comment "失败次数"
--
-- )ENGINE=InnoDB DEFAULT CHARACTER=utf8;
--
--
-- CREATE TABLE proxy (
--   id int not null auto_increment primary key,
--   proxy varchar(32) NOT NULL unique,
--   https tinyint(4) DEFAULT 0,
--   update_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `task`;
CREATE TABLE `task` (
  `task_id` varchar(36) NOT NULL COMMENT "唯一任务ID, 使用uuid4生成" ,
  `task` varchar(200) NOT NULL comment "任务的全称",
  `args` varchar(512) DEFAULT "[]" COMMENT "任务参数1",
  `kwargs` varchar(1024)  DEFAULT "{}" COMMENT "任务参数2",
  `queue` varchar(200) DEFAULT NULL COMMENT "队列",
  `exchange` varchar(200) DEFAULT NULL COMMENT "交换机",
  `routing_key` varchar(200) DEFAULT NULL COMMENT "路由",
  `finished` tinyint(1) DEFAULT 1 COMMENT "任务状态 1 待分发，2 已分发，3 成功， 4 失败",
  `priority` int DEFAULT 1 COMMENT  "优先级 1 最低 9 最高",
  `updatetime` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON update CURRENT_TIMESTAMP COMMENT "时间戳",
  PRIMARY KEY (`task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `update_task`;
CREATE TABLE `update_task` (
  `task_id` VARCHAR(36) NOT NULL  COMMENT "唯一任务ID, 使用uuid4生成" ,
  `task` varchar(200) NOT NULL comment "任务的全称",
  `error_info` TEXT DEFAULT NULL COMMENT "错误信息，如果成功，就什么也没有",
  `updatetime` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON update CURRENT_TIMESTAMP COMMENT "时间戳",
  PRIMARY KEY (`task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `hh`;
CREATE TABLE `hh` (
  `task_id` VARCHAR(36) NOT NULL  COMMENT "唯一任务ID, 使用uuid4生成" ,
  `error_info` TEXT DEFAULT NULL ,
  `hh` TEXT DEFAULT NULL,
  `update_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  PRIMARY KEY (`task_id`)
) ENGINE = InnoDB DEFAULT CHARSET=utf8;


insert into `task` (task_id, task, args) VALUES ("1", "celery_distribute_crawler.tasks.div_error", "[1, 0]");
insert into `task` (task_id, task, args) VALUES ("11", "celery_distribute_crawler.tasks.div_error", "[1, 1]");
insert into `task` (task_id, task, args) VALUES ("1111", "celery_distribute_crawler.tasks.div_error", "[1, 2]");
insert into `task` (task_id, task, args) VALUES ("11111", "celery_distribute_crawler.tasks.div_error", "[1, 3]");
insert into `task` (task_id, task, args) VALUES ("111", "celery_distribute_crawler.tasks.div_error", "[1, 0]");