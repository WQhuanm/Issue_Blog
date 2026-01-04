---
title: git常用命令随记
date: 2025-05-20 06:07:11
mathjax: true
categories: 
    - Git
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202505270031578.png
---


### 远程仓库的链接
1. git clone [options] <url>
    - -b [branch]：指定克隆某一分支

1. git switch  [branch-name] :切换分支
    + -c [local_branch_name] [remote_branch_name]：基于指定的远程分支（不指定则默认主分支）创建本地分支
    + 旧版命令为：git checkout [-b] [local_branch_name] [remote_branch_name，可选]

1. git branch :查看本地所有分支
    + -r ：查看远程分支
    + -a ：查看本地和远程所有分支
    + -d [branch_name]：删除本地分支
    + -m [old_branch_name] [new_branch_name]: 更改本地分支名
    + -vv ：列出所有本地分支及其跟踪的远程分支
    + --set-upstream-to=[远程仓库]/[远程分支] ：设置当前分支对应的远程分支

1. git init :初始本地仓库

1. git remote add [远程仓库别名] [远程仓库url] :添加一个新的远程仓库到本地（仓库别名一般是origin）

### 文件提交流程
1. git add [filename] :对指定文件添加到暂存区
    + add . :把所有已修改文件添加到暂存区

1. git commit -m "message" :将暂存区的更改提交到本地仓库，并添加提交信息
    + --amend ：补充上一个commit

1. git fetch :获取远程仓库的最新数据，但不修改本地分支

1. git pull [远程仓库名] [分支名] :从远程获取最新提交并尝试合并本地版本
    + 远程仓库名一般是默认的origin

1. git push [远程仓库名] [分支名] :将本地提交推送到远程仓库
    + -u :推送同时将本地分支追踪仓库改为此远程仓库
    + --delete ：删除远程分支
    + git push --force-with-lease [远程仓库] [远程分支] ：强行推送本地提交到远程

### 本地，远程分支间的交互
1. git status :显示当前所在本地分支，以及其追踪的远程分支

1. git branch --set-upstream-to=[remote_branch_name] [local_branch_name] :切换本地追踪的远程分支


### 文件/提交 tips
1. git stash -u ：暂存本地所有未提交修改并恢复本地到上一个提交

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

1. git revert [commit-id] ：撤回指定commit-id的提交记录