# mysql-backups
数据库自动备份（可备份至阿里云对象存储）
### 项目概述

程序为MySQL数据库定时自动备份脚本，可做到备份至阿里云OSS中，也可选择本地存储使用时需要配置mysql环境变量

### 所需的包

> * import os,time,pymysql
> * import schedule
> * import zipfile
> * import oss2

### 关键代码刨析

> 初始化程序所需变量

    ip   = input("Enter your ip: ");
    user = input("Enter your user: ");
    pwd  = input("Enter your pwd: ");
    task_time = input("Enter your task_time（--:--）: ");
    oosyes    = input("Enable OSS or not(y/n): ");
    if oosyes == 'y':
        endpoint = input("Enter your endpoint: ");
        accessKeyID = input("Enter your accessKeyID: ");
        accessKeySecret = input("Enter your accessKeySecret: ");
        bucketStr = input("Enter your bucket: ");

> 定时任务触发

此处使用轻量级python任务调度库schedule

    schedule.every().day.at(task_time).do(mainfunation)#每天指定时间段执行任务

    
