---
title: Systemd 常用命令
date: 2025-05-27 02:45:16
mathjax: true
categories: 
    - 项目管理
tags: 
    - Linux
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202506292030204.png
---


### systemctl
1. systemctl start/stop/restart/status/cat <service_name> :用于服务管理

1. systemctl enable/disable/is-enable <service_name> :设置服务自启动

1. systemctl daemon-reload :重新加载 systemd 管理的配置文件

### journalctl
1. journalctl -u <service_name> [options]
    + -u :查询指定service的日志
    + optinons
        + --no-pager :日志不分页(默认分页)
        + --since [time]:查询从指定时间段开始的日志，time 的日期格式如下（时间解析时默认使用本时区而非utc，可以使用--utc指定为utc时区）
            1. 绝对日期(可省略部分)："YYYY-MM-DD HH:MM:SS"
            1. 相对时间格式："now","today","yesterday","tomorrow" 等
        + --until [time]:查询到指定时间点结束的日志
        + -f :呈现实时日志
        + -n [num]: 查询最近num条日志

### 配置文件
#### Service 服务
1. [Unit] ：定义服务的通用信息和依赖关系
    - Description ：服务描述
    - After ：在指定服务启动后启动
    - Require ：要求指定服务能正常运行，否则当前服务停止
1. [Service] ：定义服务的具体行为
    - Type ：服务类型
        - Type=simple ：默认，长期运行服务，ExecStart启动的进程就是服务主进程
        - Type=oneshot ：一次性任务
    - User/Group ：指定执行该服务的用户/组，用于限制服务权限
    - PassEnvironment ：传递系统的环境变量（默认systemd服务启动时会清空当前进程现有的环境变量）
    - Environment ：指定环境变量(key=value)
    - EnvironmentFile ：指定环境变量文本(文本也是每行一个key=value)
    - WorkingDirectory ：指定服务进程的工作目录
    - ExecStartPre ：预处理命令（可有多个）
    - ExecStart ：服务启动的主命令
    - Restart/RestartSec ：服务异常退出时重启逻辑(always、on-failure、no)，重启间隔
    - 其余常用参数
        - AmbientCapabilities=CAP_NET_BIND_SERVICE ：允许非root用户使用特权端口(1~1024)，默认下systemd管理用户不是root，则无法使用特权端口
        - PermissionsStartOnly=true ：允许服务在启动时具有root权限，运行时恢复为指定用户/组的权限
1. [Install] ：定义服务配置自启动(enable)时的逻辑
    - WantedBy ：指定服务在哪个目标（target）下启用（如WantedBy=multi-user.target，在多用户模式下启动）  

##### 例子
```shell
# /usr/lib/systemd/system/example.service
[Unit]
Description=example web server 
After=network.target

[Service]
Type=simple
User=wq
PassEnvironment=HOST_NAME
Environment="RUN_ENV=test"
WorkingDirectory=/opt/example
ExecStart=/opt/example/run.sh
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
```
 
#### Timer 定时器（一般用于定时启动同名服务）
1. [Unit],[Install] 模块和service类似
1. [Timer] ：定义定时器行为
    - OnCalendar ：（cron语法，指定定时时间）
    - RandomizedDelaySec ：增加一个执行时间随机延迟
    - Persistent ：确保因停机等原因导致错过的任务，在启动时重新执行

##### 例子
```shell
# /usr/lib/systemd/system/certbot-renew.timer
[Unit]
Description=This is the timer to set the schedule for automated renewals

[Timer]
OnCalendar=*-*-* 00/12:00:00
RandomizedDelaySec=12hours
Persistent=true

[Install]
WantedBy=timers.target
```


#### 启用 Systemd 服务
1. 将service文件放于特定目录（如：/usr/lib/systemd/system/）
1. 重新加载 systemd 配置：sudo systemctl daemon-reload
1. 服务设置为开机自启：sudo systemctl enable [service服务]

### 参考
[Systemd 入门教程：命令篇](https://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-commands.html)  
[Systemd 入门教程：实战篇](https://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-part-two.html)  