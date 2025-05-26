---
title: 远程服务器连接与使用（Putty）
date: 2025-05-26 06:55:37
mathjax: true
categories: 
    - CS技术
tags: 
    - CS技术
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202505270032825.png
---


 1. 桌面机到远程服务器的连接：Putty
    1. Putty的pageant.exe 添加证书CAPI Cert（证书用yubikey安装）
    1. 与跳板机建立连接（如果需要的话）
        + 在session设置跳板机ip（默认端口22）
        + 在connectio-Data设置默认登录用户名
    1. 通过跳板机与服务器建立连接
        + 在session设置目标服务器ip（默认端口22）
        + 在connectio-Data设置默认登录用户名
        + 在connection-Proxy配置跳板机
            + Proxy type: Local
            + 发送到代理的命令: plink -P %proxyport %user@%proxyhost -nc %host:%port

1. 桌面机与服务器的文件传输：pscp
    + pscp [options] 本地文件位置/远程服务器文件位置 远程服务器文件位置/本地文件位置
        + -r:递归复制，复制整个目录
