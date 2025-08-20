---
title: Docker的使用
date: 2025-04-07 12:34:48
mathjax: true
categories: 
    - Web后端
tags: 
    - Docker
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202504101117974.png
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
    + 容器内部执行命令：docker exec -it 容器名 执行的命令(如bash：打开容器的交互式终端)
    + 删除容器：docker rm 
    + 查看运行容器的详情信息：docker ps
    + 宿主/容器文件传输：docker cp win文件路径 容器名:容器目标文件路径

1. Docker 卷（volume，用于可持久化容器内部数据）命令：基本常见的docker命令中间加个volume就能执行（eg：docker volume inspect 卷名）
    1. windows的wsl的docker卷位置（与容器内部文件一一映射）
        + 较新版本的docker的volume在windows的挂载位置是：\\wsl$\docker-desktop\mnt\docker-desktop-disk\data\docker\volumes
        + 较旧版本的位置是： \\wsl$\docker-desktop-data\data\docker\volumes
    1. win文件传输到容器内部路径的方式
        1. 使用docker cp
        1. win的资源管理器直接定位到docker卷位置，把文件复制过去即可
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

---
title: Docker的使用
date: 2025-04-07 12:34:48
mathjax: true
categories: 
    - Web后端
tags: 
    - Docker
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202504101117974.png
---


### 常用Docker命令
- 容器相关
    - docker run [options] [镜像名] ：创建并运行容器
        + --name：容器名字
        + -d：容器可后台运行
        + -p：宿主机和容器间的端口映射(不指定映射则无法外部访问)
        + -v：指定挂载的数据卷（-v <本地卷路径>:<容器内部路径>，eg：-v rabbitmq_data:/var/lib/rabbitmq）
        + -it：-t启用容器终端，-i允许与容器终端交互
        + -e：环境变量
    - docker exec -it [容器名] [执行的命令(如bash)] ：容器内部执行命令
    - docker cp [源文件路径] [目的传输路径] ：宿主容器间文件传输（容器路径为：容器名:路径）
    - docker rm [容器名] ：删除容器
    - docker ps ：显示所有正在运行的容器信息
        - -a ：显示所有容器
    - docker inspect [容器/镜像/网络/卷] ：查看详情底层信息

- 镜像相关 
    - docker images ：获取下载的所有镜像信息，镜像的名称是REPOSITORY:TAG
    - docker search [关键字] ：从仓库搜索相关镜像
    - docker pull [镜像名] ：下载镜像
    - docker rmi [镜像名] ：删除镜像
    - docker build [options] [上下文路径] ：构建镜像
        - 参数
            - -t [镜像名:TAG] ：
            - 
        - 上下文路径 ：docker构建时需要使用的本地文件所在目录（一般用. 表示当前目录，未指定则默认DockerFile所在目录）
            - docker构建时又docker引擎执行，无法访问本地文件，因此需要指定后打包该目录下**所有内容**
    - docker commit [容器名] [镜像名] ：将指定容器制作成镜像
    - docker save -o [宿主机路径] [镜像] ：将镜像压缩并保存到本地(.tar 文件)
    - docker load -i [镜像路径] ：将保存的镜像解压至docker

### Docker 容器
1. Docker 卷（volume，用于可持久化容器内部数据）
    - windows的wsl的docker卷位置（与容器内部文件一一映射）
        + 较新版本的docker的volume在windows的挂载位置是：\\wsl$\docker-desktop\mnt\docker-desktop-disk\data\docker\volumes
        + 较旧版本的位置是： \\wsl$\docker-desktop-data\data\docker\volumes

### DockerFile
> Docker 的镜像是分层的，每执行一条指令都会建立新一层（这一层只包含该指令所带来的文件系统变更）
    - RUN指令合并可以有效减少镜像层数，避免镜像体积膨胀

#### 常用文件指令
1. FROM [镜像]：指定构建新镜像所基于的基础镜像，后续指令基于该镜像执行
1. ARG [变量]：指定构建时的变量
    - 执行docker build时可 通过 --build-arg key=val 赋值变量（覆盖原本的值） ，每个--build-arg只传递一对key-value
    - ARG 变量在FROM之前，则在FROM命令后无效（这种变量一般用于指定from 镜像的版本等参数）
1. RUN [shell命令] ：执行shell命令
1. COPY [源路径] [目标路径]：将文件或目录复制到镜像中
1. ENV [key=value] ：在容器内部设置环境变量
1. WORKDIR [path] ：设置后续指令的工作目录

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

---
title: Docker的使用
date: 2025-04-07 12:34:48
mathjax: true
categories: 
    - Web后端
tags: 
    - Docker
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202504101117974.png
---


### 常用Docker命令
- 容器相关
    - docker run [options] [镜像名] ：创建并运行容器
        + --name：容器名字
        + -h(--hostname) ：设定容器主机名
        + -d：容器可后台运行
        + -p：宿主机和容器间的端口映射(不指定映射则无法外部访问)
        + -v：指定挂载的数据卷（-v <本地卷路径>:<容器内部路径>，eg：-v rabbitmq_data:/var/lib/rabbitmq）
        + -it：-t启用容器终端，-i允许与容器终端交互
        + -e：环境变量
        + --cap-add ：开启指定的linux内核权限
            - NET_ADMIN ：网络权限
            - SYS_PTRACE ：允许使用 ptrace 系统调用
        + --privileged ：特权模式运行容器
    - docker exec -it [容器名] [执行的命令(如bash)] ：容器内部执行命令
    - docker cp [源文件路径] [目的传输路径] ：宿主容器间文件传输（容器路径为：容器名:路径）
    - docker rm [容器名] ：删除容器
    - docker ps ：显示所有正在运行的容器信息
        - -a ：显示所有容器
    - docker inspect [容器/镜像/网络/卷] ：查看详情底层信息

- 镜像相关 
    - docker images ：获取下载的所有镜像信息，镜像的名称是REPOSITORY:TAG
    - docker search [关键字] ：从仓库搜索相关镜像
    - docker pull [镜像名] ：下载镜像
    - docker rmi [镜像名] ：删除镜像
    - docker build [options] [上下文路径] ：构建镜像
        - 参数
            - -t [镜像名:TAG] ：
            - 
        - 上下文路径 ：docker构建时需要使用的本地文件所在目录（一般用. 表示当前目录，未指定则默认DockerFile所在目录）
            - docker构建时又docker引擎执行，无法访问本地文件，因此需要指定后打包该目录下**所有内容**
    - docker commit [容器名] [镜像名] ：将指定容器制作成镜像
    - docker save -o [宿主机路径] [镜像] ：将镜像压缩并保存到本地(.tar 文件)
    - docker load -i [镜像路径] ：将保存的镜像解压至docker
    - docker push [仓库地址/]镜像名[:tag] ：把镜像推送到仓库
        - 不指定仓库地址时，默认推送到docker.io

### Docker 容器
1. Docker 卷（volume，用于可持久化容器内部数据）
    - windows的wsl的docker卷位置（与容器内部文件一一映射）
        + 较新版本的docker的volume在windows的挂载位置是：\\wsl$\docker-desktop\mnt\docker-desktop-disk\data\docker\volumes
        + 较旧版本的位置是： \\wsl$\docker-desktop-data\data\docker\volumes

### DockerFile
> Docker 的镜像是分层的，每执行一条指令都会建立新一层（这一层只包含该指令所带来的文件系统变更）
    - RUN指令合并可以有效减少镜像层数，避免镜像体积膨胀

#### 常用文件指令
1. FROM [镜像]：指定构建新镜像所基于的基础镜像，后续指令基于该镜像执行
1. ARG [变量]：指定构建时的变量
    - 执行docker build时可 通过 --build-arg key=val 赋值变量（覆盖原本的值） ，每个--build-arg只传递一对key-value
    - ARG 变量在FROM之前，则在FROM命令后无效（这种变量一般用于指定from 镜像的版本等参数）
1. RUN [shell命令] ：执行shell命令
1. COPY [源路径] [目标路径]：将文件或目录复制到镜像中
1. ENV [key=value] ：在容器内部设置环境变量
1. WORKDIR [path] ：设置后续指令的工作目录

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

---
title: Docker的使用
date: 2025-04-07 12:34:48
mathjax: true
categories: 
    - Web后端
tags: 
    - Docker
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202504101117974.png
---


### 常用Docker命令
- 容器相关
    - docker run [options] [镜像名] ：创建并运行容器
        + --name：容器名字
        + -h(--hostname) ：设定容器主机名
        + -d：容器可后台运行
        + -p：宿主机和容器间的端口映射(不指定映射则无法外部访问)
        + -v：指定挂载的数据卷（-v <本地卷路径>:<容器内部路径>，eg：-v rabbitmq_data:/var/lib/rabbitmq）
        + -it：-t启用容器终端，-i允许与容器终端交互
        + -e：环境变量
        + --cap-add ：开启指定的linux内核权限
            - NET_ADMIN ：网络权限
            - SYS_PTRACE ：允许使用 ptrace 系统调用
        + --privileged ：特权模式运行容器
    - docker exec -it [容器名] [执行的命令(如bash)] ：容器内部执行命令
    - docker cp [源文件路径] [目的传输路径] ：宿主容器间文件传输（容器路径为：容器名:路径）
    - docker rm [容器名] ：删除容器
    - docker rename [当前名称] [新名称] ：容器重命名
    - docker ps ：显示所有正在运行的容器信息
        - -a ：显示所有容器
    - docker inspect [容器/镜像/网络/卷] ：查看详情底层信息

- 镜像相关 
    - docker images ：获取下载的所有镜像信息，镜像的名称是REPOSITORY:TAG
    - docker search [关键字] ：从仓库搜索相关镜像
    - docker pull [镜像名] ：下载镜像
    - docker rmi [镜像名] ：删除镜像
    - docker build [options] [上下文路径] ：构建镜像
        - 参数
            - -t [镜像名:TAG] ：
            - 
        - 上下文路径 ：docker构建时需要使用的本地文件所在目录（一般用. 表示当前目录，未指定则默认DockerFile所在目录）
            - docker构建时又docker引擎执行，无法访问本地文件，因此需要指定后打包该目录下**所有内容**
    - docker commit [容器名] [镜像名] ：将指定容器制作成镜像
    - docker save -o [宿主机路径] [镜像] ：将镜像压缩并保存到本地(.tar 文件)
    - docker load -i [镜像路径] ：将保存的镜像解压至docker
    - docker push [仓库地址/]镜像名[:tag] ：把镜像推送到仓库
        - 不指定仓库地址时，默认推送到docker.io

### Docker 容器
1. Docker 卷（volume，用于可持久化容器内部数据）
    - windows的wsl的docker卷位置（与容器内部文件一一映射）
        + 较新版本的docker的volume在windows的挂载位置是：\\wsl$\docker-desktop\mnt\docker-desktop-disk\data\docker\volumes
        + 较旧版本的位置是： \\wsl$\docker-desktop-data\data\docker\volumes

### DockerFile
> Docker 的镜像是分层的，每执行一条指令都会建立新一层（这一层只包含该指令所带来的文件系统变更）
    - RUN指令合并可以有效减少镜像层数，避免镜像体积膨胀

#### 常用文件指令
1. FROM [镜像]：指定构建新镜像所基于的基础镜像，后续指令基于该镜像执行
1. ARG [变量]：指定构建时的变量
    - 执行docker build时可 通过 --build-arg key=val 赋值变量（覆盖原本的值） ，每个--build-arg只传递一对key-value
    - ARG 变量在FROM之前，则在FROM命令后无效（这种变量一般用于指定from 镜像的版本等参数）
1. RUN [shell命令] ：执行shell命令
1. COPY [源路径] [目标路径]：将文件或目录复制到镜像中
1. ENV [key=value] ：在容器内部设置环境变量
1. WORKDIR [path] ：设置后续指令的工作目录

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

