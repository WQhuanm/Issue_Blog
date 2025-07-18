---
title: Systemd 常用命令
date: 2025-05-27 02:45:16
mathjax: true
categories: 
    - Linux
tags: 
    - Linux
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202506292030204.png
---


### systemctl
1. systemctl start/stop/restart/status/cat <service_name> :用于服务管理

1. systemctl enable/disable/is-enable <service_name> :设置服务自启动

1. systemctl daemon-reload :重新加载 systemd 管理的配置文件

### journalctl
1. journalctl -u <service_name> [options1] [options2]
    + -u :查询指定service的日志
    + optinons1
        + --no-pager :日志不分页(默认分页)
        + --since [time]:查询从指定时间段开始的日志，time 的日期格式如下（时间解析时默认使用本时区而非utc，可以使用--utc指定为utc时区）
            1. 绝对日期(可省略部分)："YYYY-MM-DD HH:MM:SS"
            1. 相对时间格式："now","today","yesterday","tomorrow" 等
        + --until [time]:查询到指定时间点结束的日志
    + optins2
        + -f :呈现实时日志
        + -n [num]: 查询最近num条日志

### 配置文件 :TODO



#### Service
1. 常用参数
    + AmbientCapabilities=CAP_NET_BIND_SERVICE ：允许非root用户使用特权端口(1~1024)，默认下systemd管理用户不是root，则无法使用特权端口

#### 启用 Systemd 服务
1. 将service文件放于特定目录（如：/usr/lib/systemd/system/）
1. 重新加载 systemd 配置：sudo systemctl daemon-reload
1. 服务设置为开机自启：sudo systemctl enable [service文件]

### 参考
[Systemd 入门教程：命令篇](https://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-commands.html)  
[Systemd 入门教程：实战篇](https://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-part-two.html)  
