---
title: MySQL基础知识随记
date: 2025-03-15 10:15:51
categories: 
    - MySQL
tags: 
    - MySQL
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202502211226091.png
---

1. varchar(m)
    + 最多可以存储m个字符(一个汉字也是一个字符，如果是mysql 4.0以下，m指的是字节)
    + 占用内存：实际字符+额外字节（用于统计字符串长度，字符串字节数<=255B,1个额外字节存储，否则2个）
    + GBK：中文字符占2个字节；UTF-8：中文字符占3个字节

1. int（10）
    + 10表示显示宽度，默认不足空格填充
