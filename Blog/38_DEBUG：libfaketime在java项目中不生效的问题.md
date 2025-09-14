---
title: DEBUG：libfaketime在java项目中不生效的问题
date: 2025-06-23 06:13:21
mathjax: true
categories: 
    - DEBUG
tags: 
    - Java
    - Linux
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202412222015910.png
---


> 问题背景：在docker容器上部署的java项目，需要通过修改系统时间进行cookie过期测试，然而libfaketime引入后却不生效  
先说结论：jdk版本问题

1. 发现不生效后，我首先确认是否存在LD_PRELOAD这个关键的环境变量，发现项目的systemd服务是存在的，但是java项目运行时却没有
1. 进一步排查发现root用户下运行服务，libfaketime生效，而以普通用户去管理服务，则不生效。此时猜测用户权限不够（可能是吧，但是后续找不到突破口）
1. 在[libfaketime](https://github.com/wolfcw/libfaketime)的issue逛了一圈，看看能不能借鉴前人智慧，发现作者曾说过有可能是jdk底层使用的函数，faketime不支持拦截
    ![](https://cdn.jsdelivr.net/gh/WQhuanm/Img_repo_1/img/20250623125549611.png)
1. 接着我在虚拟机上尝试复现服务器上的问题，发现jdk1.8和jdk11（虚拟机是11.0.23,服务器是11.0.6）在root和普通用户下libfaketime均能生效！
1. 保险起见，我在服务器上使用C语言代码测试，发现faketime也能起效
1. 这时几乎可以断定是jdk的问题了，升级到11.0.23即可
