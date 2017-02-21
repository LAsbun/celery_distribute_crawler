CREATE  TABLE task(
'task' VARCHAR(256) not null "任务名称",
'auguments' TEXT DEFAULT "NULL" COMMENT "任务参数 默认是NULL 无参",
'priority' int not NULL DEFAULT 0 COMMENT "优先级 0 最低",
'updatetime' TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT "时间戳",
'fail' int DEFAULT 0 comment "失败次数"

)ENGINE=InnoDB DEFAULT CHARACTER=utf8;