---
title: git常用命令随记
date: 2025-05-20 06:07:11
mathjax: true
categories: 
    - GitHub
tags: 
    - GitHub
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202505270031578.png
---


### 远程仓库的链接
1. git clone <url>

1. git switch [-c] <new-branch-name> :切换分支
    + -c：可选，会尝试创建当前不存在的新分支
    + 旧版命令为：git checkout [-b] <new-branch_name>

1. git branch [-r/-a]:查看本地所有分支
    + -r :可选，查看远程分支
    + -a :可选，查看本地和远程所有分支

### 文件提交流程
1. git add [filename] :对指定文件添加到暂存区
    + add . :把所有已修改文件添加到暂存区

1. git commit -m "message" :将暂存区的更改提交到本地仓库，并添加提交信息

1. git fetch :获取远程仓库的最新数据，但不修改本地分支

1. git pull [远程仓库名] [分支名] :从远程获取最新提交并尝试合并本地版本
    + 远程仓库名一般是默认的origin

1. git push [远程仓库名] [分支名] :将本地提交推送到远程仓库

### 文件/提交 tips
1. git restore [--staged] [filename] :将指定文件恢复到暂存区/最新提交的状态
    + 上述命令的旧版写法是：git checkout -- [filename]
    + --staged :可选，将指定文件在暂存区的缓存删除


1. git rebase -i :在变基过程中编辑、删除或合并提交
    + pick：保留提交
    + reword：修改提交信息
    + edit：编辑提交
    + squash：将当前提交与前一个提交合并
    + fixup：将当前提交与前一个提交合并，不保留提交信息
    + drop：删除提交

1. git log :查看历史commit记录

1. git reset [--hard] HEAD :清空暂存区
    + --hard :将本地仓库回溯到最近一次提交

