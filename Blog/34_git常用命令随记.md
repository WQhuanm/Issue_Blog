---
title: git常用命令随记
date: 2025-05-20 06:07:11
mathjax: true
categories: 
    - Git
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202505270031578.png
---


> git <command> -h ：查看命令手册

### 远程/本地分支交互

1. git clone <仓库 url>

   - -b [branch]：指定克隆某一分支

1. git init :初始本地仓库

1. git remote

   - -v ：列出已配置的远程仓库名称及对应的仓库 rul
   - add <仓库别名> <仓库 url> ：新增一个远程仓库到本地（别名一般为 origin）
   - remove <仓库别名> ：删除一个远程仓库配置

1. git status :显示工作区状态

1. git log :查看历史 commit 记录

### 本地分支操作

1. git switch [branch-name] :切换分支

   - -c [local_branch_name] [remote_branch_name]：基于指定的远程分支（不指定则默认主分支）创建本地分支
   - 旧版命令为：git checkout [-b] [local_branch_name] [remote_branch_name，可选]

1. git branch :查看本地所有分支

   - -a/-r ：查看本地和远程所有分支/只查看远程分支
   - -d [branch_name]：删除本地分支
   - -m [old_branch_name] [new_branch_name]: 更改本地分支名
   - -vv ：列出所有本地分支及其跟踪的远程分支
   - -u `<repo>/<remote_branch_name> <local_branch_name>` :切换本地追踪的远程分支

### 文件提交流程

> 可以先 git rebase 刷新当前分支起点（避免本地历史 commit 影响）

1. git add [filename] :对指定文件添加到暂存区

   - . :把所有已修改文件添加到暂存区

1. git commit -m "message" :将暂存区的更改提交到本地仓库，并添加提交信息

   - --amend ：补充上一个 commit

1. git fetch : 获取所有远程分支最新数据

1. git pull `<repo> <branch>` :从远程获取最新提交并尝试合并本地版本

1. git push `<repo> <branch>` :将本地提交推送到远程仓库
   - -u :推送同时将本地分支追踪仓库改为此远程仓库
   - --delete ：删除远程分支

### 本地文件操作

1. git stash ：暂存工作区未提交的改动（包括暂存区）到栈，用于切换分支/拉取更新后，再回复改动

   - -u ：未跟踪文件的修改也进行暂存
   - pop ：恢复暂存改动到工作区并从栈删除该暂存条目
   - apply ：恢复暂存改动到工作区，但不从栈删除该暂存条目

1. git cherry-pick <commit-sha> ：挑选某些 commit 加入到当前分支

   - -n ：只应用所选 commit 产生的改动，但不应用为当前分支的 commit

1. git restore [filename] :将指定文件恢复到暂存区/最新提交的状态

   - 上述命令的旧版写法是：git checkout -- [filename]
   - --staged ：将指定文件在暂存区的缓存删除

1. git rebase [repo]/[remote_branch] ：将当前分支的起点变基为与指定远程分支的最近祖先上（重写当前分支的父链）

   - -i ：交互式变基，在变基过程中人工编辑提交信息
     - pick：保留提交
     - reword：修改提交信息
     - edit：编辑提交
     - squash：将当前提交与前一个提交合并
     - fixup：将当前提交与前一个提交合并，不保留提交信息
     - drop：删除提交

1. git reset HEAD :清空暂存区

   - --hard :将本地仓库回溯到最近一次提交

1. git revert [commit-id] ：撤回指定 commit-id 的提交记录
