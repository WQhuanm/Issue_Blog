---
title: docker常用镜像的部署配置
date: 2025-07-21 03:05:44
mathjax: true
categories: 
    - 项目管理
tags: 
    - Docker
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202507270022983.png
---


```shell
# postgresql
docker pull postgres:13.21-alpine3.20
docker run -itd --name postgresql -p 5432:5432 -v pg_data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=1234 postgres:13.21-alpine3.20

# Mongo
docker pull mongo
docker run -itd --name mongodb -p 27017:27017 -v mongo_data:/var/lib/mongo/data -e MONGO_INITDB_ROOT_USERNAME=root  -e  MONGO_INITDB_ROOT_PASSWORD=1234   mongo

# rabbitmq
docker pull rabbitmq:management
docker run -itd --name rabbitmq -p 5672:5672 -p 15672:15672 -v rabbitmq_data:/var/lib/rabbitmq -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=1234 rabbitmq:management

# zookeeper
docker pull zookeeper
docker run -itd --name zookeeper -p 2181:2181 zookeeper -v zookeeper_data:/var/lib/zookeeper  zookeeper
```