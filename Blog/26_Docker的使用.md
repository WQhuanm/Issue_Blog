---
title: Docker的使用
date: 2025-04-07 12:34:48
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202504072032101.png
---

### 常用命令
1. 镜像命令
    + 获取下载的所有镜像（显示镜像的仓库源、标签（镜像版本）、id...），镜像的名称就是REPOSITORY:TAG（eg：rabbitmq:management）：docker images
    + 从仓库搜索相关镜像：docker search 关键字
    + 下载镜像到本地（镜像只指定仓库时，会使用默认tag）：docker pull 镜像名
    + 删除镜像：docker rmi 镜像名
    + 创建并允许容器：docker run [可选参数] 镜像名 
        1. 常见参数如下：
            + --name：容器名字
            + -d：容器可后台运行
            + -p：宿主机和容器间的端口映射(不指定映射则无法外部访问)
            + -v：指定挂载的数据卷（-v <本地卷路径>:<容器内部路径>，eg：-v rabbitmq_data:/var/lib/rabbitmq）
            + -it：-t启用容器终端，-i允许与容器终端交互
            + -e：环境变量
        
1. 容器命令
    + 容器内部执行命令：docker exec -it 容器名 执行的命令(如/bin/bash：打开容器的交互式终端)
    + 删除容器：docker rm 
    + 查看运行容器的详情信息：docker ps

1. Docker 卷（volume，用于可持久化容器内部数据）命令：基本常见的docker命令中间加个volume就能执行（eg：docker volume inspect 卷名）

1. 容器制作成镜像与镜像保存/解压
    + 将容器制作成镜像：docker commit 容器名 镜像名
    + 将镜像保存到宿主机当前文件夹下：docker save -o 宿主机目标文件名（可以命名为.tar文件） 镜像名
    + 镜像解压：docker load -i 文件路径


### 附：Docker的安装
> [docker及汉化包](https://github.com/asxez/DockerDesktop-CN)
1. D盘安装：cmd执行："D:\DockerDesktop-installer.exe" install --installation-dir="D:\My_Soft\Docker"  （安装包 install --installation-dir=目标安装路径（需要先创建好相应文件夹）

1. settings的资源部分，更改镜像保存位置为D盘

1. 添加docker镜像（setting的docker 引擎部分）
    ```json
    "registry-mirrors": [
        "https://docker.mirrors.ustc.edu.cn",
        "https://registry.docker-cn.com"
    ]
    ```


