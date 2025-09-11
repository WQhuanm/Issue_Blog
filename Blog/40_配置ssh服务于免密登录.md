---
title: 配置ssh服务于免密登录
date: 2025-06-29 14:38:40
mathjax: true
categories: 
    - 项目管理
tags: 
    - Linux
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202506292238854.png
---


1. 需要确保目标服务器安装ssh服务
```shell
sudo apt-get install openssh-server
sudo /etc/init.d/ssh start
```
1. ssh服务首先都是桌面机生成ssh密匙：ssh-keygen（一般保存于C:\Users\user\.ssh 目录下,目录内文件如下）
    + config：配置允许免密登录的服务
    + id_rsa.pub：公匙，提供给目标ssh服务
    + id_rsa：私匙，不能泄露

1. 桌面机在config文件配置免密登录的格式如下
``` shell
Host 服务器别名
    HostName 目标的ip/域名
    User 服务器登录的用户名（配置GitHub等可以没有）
    Port 一般可默认不指定

# 比如
Host ubuntut18
    HostName 192.168.63.131
    User wqhuanm

Host github.com
    Hostname ssh.github.com
    Port 443
```

1. 目标服务器的/home/user/.ssh 文件夹下
    + 生成一个authorized_keys（存放多个公匙）
    + 将桌面机生成的id_rsa.pub放入

