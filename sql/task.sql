CREATE  TABLE task(
task VARCHAR(256) not null "任务名称",
auguments TEXT DEFAULT "NULL" COMMENT "任务参数 默认是NULL 无参",
priority int not NULL DEFAULT 0 COMMENT "优先级 0 最低",
updatetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT "时间戳",
fail int DEFAULT 0 comment "失败次数"

)ENGINE=InnoDB DEFAULT CHARACTER=utf8;


CREATE TABLE proxy (
  id int not null auto_increment primary key,
  proxy varchar(32) NOT NULL unique,
  https tinyint(4) DEFAULT 0,
  update_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8


"""
CREATE TABLE `task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL COMMENT "这里是任务的唯一id",
  `task` varchar(200) NOT NULL comment "任务",
  `args` longtext NOT NULL COMMENT "任务参数1",
  `kwargs` longtext NOT NULL COMMENT "任务参数2",
  `queue` varchar(200) DEFAULT NULL COMMENT "队列",
  `exchange` varchar(200) DEFAULT NULL “”,
  `routing_key` varchar(200) DEFAULT NULL,
  `finished` tinyint(1) DEFAULT 0 COMMENT "1 待分发，2 已分发，3 成功， 4 失败",
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
"""