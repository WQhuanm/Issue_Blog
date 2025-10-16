---
title: Redis学习笔记
date: 2025-03-03 08:50:15
mathjax: true
categories: 
    - Web后端
tags: 
    - Redis
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202501262318741.jpeg
---

### 缓存读写策略（如何保证缓存和数据库数据的一致性）
1. Cache Aside Pattern（旁路缓存模式）：读多写少（写多影响cache命中率，因为写了删cache）
    + 写：先更新 db，然后直接删除 cache 。（保证删cache成功策略：增加重试机制，或引入消息队列异步删除）
    + 读：从 cache 中读取数据，读取到就直接返回。读取不到的话，就从 db 中读取数据返回，再把数据放到 cache 中。
    + 写操作不先删cache后更新DB：因为删完还没更新DB，读的都是旧数据
    + 选择删cache而不是更新cache原因：
        1. 存在sessionA先到，sessionB后到但是先更新完cache，然后sessionA才更新cache，导致数据错误
        1. 更新的cache不一定后面会用到
    + 写策略存在的问题：（小概率，因为cache写比DB写快）
        1. 无cache时，sessionA读完旧数据写cache
        1. sessionB更新DB数据，cache还没写故不用删cache
        1. sessionA写入cache为旧数据，DB的才是新数据
1. Read/Write Through Pattern（读写穿透）：数据一致性要求高，且读写操作频繁的场景。
    + 写：cache 中存在，则先更新 cache，然后 cache 服务自己更新 db（同步更新 cache 和 db）。否则直接更新 db。
    + 读：从 cache 中读取数据，读取到就直接返回。读取不到的话，就从 db 中读取数据返回，再把数据放到 cache 中。 
1. Write Behind Pattern（异步缓存写入）：写操作频繁且对实时一致性要求不高的场景
    写：只更新缓存，不直接更新 db，而是改为异步批量的方式来更新 db

### 持久化机制
#### 1. RDB（Redis Database Backup,快照）
+ Redis 可以通过创建快照来获得存储在内存里面的数据在某个时间点上的副本（压缩的二进制数据，文件小，恢复数据直接解析文件即可），一定时间内数据变换越快，越快触发RDB持久，默认RDB fork 出一个子进程执行快照任务（但每次快照全部数据还是慢）
+ BGSAVE使用子进程执行（默认使用），SAVE使用主线程执行，会阻塞其他命令
    + BGSAVE快照核心：fock的写时复制
    + 写时复制存在的问题：如果修改大key，主进程需要大量时间阻塞来复制新内存页

#### 2. AOF（append-only file,只追加文件 ）
+ AOF 持久化会把所有更改 Redis 中的数据的命令写入到 AOF文件（执行完命令再写入，避免写入时阻塞当前命令）
+ 持久化方式（fsync策略）

    appendfsync always：每次write写到系统内核缓冲区后，会立刻把数据同步到磁盘的AOF文件

    appendfsync everysec：write完立即返回，fsync每秒同步一次 AOF 文件

    appendfsync no：write完立即返回，让操作系统决定何时进行同步
+ 工作流程
    + 所有的写命令会追加（append）到 AOF 缓冲区中
    + 再将 AOF 缓冲区的数据写入（write，系统调用）到系统内核缓冲区
    + 根据文件同步策略（fsync，系统调用）将系统内核缓冲区内容同步到磁盘
    + 随着 AOF 文件越来越大，需要定期对 AOF 文件进行文件重写（读取所有缓存的键值对数据，并为每个键值对生成一条命令），达到压缩的目的
        + 子进程执行重写：利用fock的写时复制，子进程和父进程共享内存，减少内存复制开销。同时保证主进程修改数据时子进程的重写不受影响
        + 期间服务器的命令则记录在重写缓冲区
        + 新日志重写完后，主进程收到信号，把重写缓冲区的内容追加到新aof文件，然后覆盖旧aof文件
    + 当 Redis 重启时，可以加载 AOF 文件进行数据恢复（重启加载,load），恢复需要依次执行每个写命令日志的命令，速度慢，因此不建议单独使用
+ AOF 校验机制：校验和（checksum，使用CRC64），checksum存在于AOF文件尾部来检验
+ 开启AOF时优先使用AOF来还原数据库

#### 3. RDB 和 AOF 的混合持久化
+ 修改了原本重写AOF的流程
+ fork 的重写子进程会先将与主线程共享的内存数据以 RDB 方式写入到 AOF 文件，期间主线程的操作写在重写缓冲区
+ RDB写完时，再把重写缓冲区的内容追加到文件尾部（主进程执行）
+ 平时的命令还是以aof格式写入aof文件

### Redis单线程模型
1. Redis 的性能瓶颈不在 CPU ，主要在内存和网络，所以事件处理器单线程更为简单
1. Redis的文件事件处理器（file event handler）是单线程方式运行，有4大部分组成
    + 多个 socket（客户端连接）
    + IO 多路复用程序（监听socket连接,一个线程来检查多个 Socket 的就绪状态）
    + 文件事件分派器（将 socket 关联到相应的事件处理器）
    + 事件处理器
1. 其多线程的应用
    1. 增加了针对bigkey删除操作的“异步处理”命令，使用其他线程完成，如unlink（同del功能，但是del在主线程删除）
    1. 多线程处理网络请求（提高网络 IO 读写性能）


### 内存管理
1. 过期字典：过期字典保存数据过期的时间。查询key时，首先检查该 key 是否存在于过期字典中（时间复杂度为 O(1)），如果不在就直接返回，在的话需要判断一下这个 key 是否过期，过期直接删除 key 然后返回 null。
1. 过期 key 删除策略(定期删除+惰性删除结合)
    1. 惰性删除：只会在取出/查询 key 的时候才对数据进行过期检查。对CPU友好
    1. 定期删除：周期性地随机从设置了过期时间的 key 中抽查一批，删除其中的过期key，如果这一批过期的 key 比例超过一个比例，就会重复执行此删除流程,直到低于这个比例或超过执行时间，才中断这一次定期删除循环。对内存友好
    1. lazy free 机制：开启后，对于过期的bigkey，会在后台异步删除
1. 内存淘汰策略（只有在运行内存达到了配置的最大内存阈值时才会触发）
    1. no-eviction（默认内存淘汰策略）：禁止驱逐数据，当内存不足以容纳新写入数据时，新写入操作会报错。
    1. volatile-lru（least recently used）：从已设置过期时间的数据中挑选最近最少使用的数据淘汰。
    1. allkeys-lru（least recently used）：从数据集中移除最近最少使用的数据淘汰。
    1. volatile-ttl：从已设置过期时间的数据中挑选将要过期的数据淘汰。
    1. volatile-random：从已设置过期时间的数据中任意选择数据淘汰。
    1. allkeys-random：从数据集中任意选择数据淘汰。
    1. volatile-lfu（least frequently used）：从已设置过期时间的数据中挑选最不经常使用的数据淘汰。
    1. allkeys-lfu（least frequently used）：从数据集中移除最不经常使用的数据淘汰。
       
### 性能优化
+ 使用Lua脚本批量操作多条命令。减少网络传输消耗（注：Lua脚本运行时出错并中途结束，之后的操作不会进行，但是之前已经发生的写操作不会撤销）

### 缓存穿透、缓存击穿、缓存雪崩（数据库被请求不断直击）
1. 缓存穿透（非法key，不存在于缓存中和数据库中）
    1. 缓存无效 key，设置短过期时间
    1. 布隆过滤器，存在的值都缓存在布隆过滤器中（类似hash），合法的值一定在布隆过滤器存在，非法的大概率不存在
1. 缓存击穿（热点key，不在缓存）
    + 针对热点数据提前预热缓存，修改时加锁，只有一个请求可查询并更新
    + 加互斥锁，cache过期只有拿到锁的才能访问DB
1. 缓存雪崩（大量key消失）
    1. 如果是redis不可用，应提升redis
        1. 采用 Redis 集群
        1. 设置多级缓存
    1. 就是key大量失效
        1. 设置随机TTL
        1. 提前预热，并让特定场景key在场景结束前不过期
            

### 五种基本value类型（key都是string，value的基本元素也是string）
- string ：（底层使用**Simple Dynamic String (SDS)**，简单动态字符串实现，会预分配一段内存来存储字符串）
    - 常用命令 ：`SET key value`,`GET key`,`MSET key1 val1 key2 val2`（批量设置）
- hash ：哈希表，用于存储对象等，内部可容纳多个key-value，减少了redis的key数量
    - 常用命令 ：`HSET key field value`,`HGET key field`,`HGETALL key`,`HMSET key field1 v1`(批量设置)
- list
    - 常用命令 ：`LPUSH/RPUSH key value`,`LPOP/RPOP key`,`LRANGE/RRANGE key start stop` (获取范围内的元素)
- set
    - 常用命令 ：`SADD key val`,`SMEMBERS key`(获取所有元素),`SISMEMBER key val`(判断元素是否存在),`SREM key val`(移除元素),`SUNION/SINTER/SDIFF`(集合运算)
- z-set ：使用跳表实现
    ![](https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202503262038882.png)
    - 常用命令 ：`ZADD key score val`,`ZRANGE/ZREVRANGE key start stop [WITHSCORES]` (按索引范围升序/降序获取),`ZRANGEBYSCORE key min max`(按分数范围获取),`ZSCORE key val`(获取元素的分数)

### 常用数据结构及其底层数据
- HyperLogLog：基数估算（标准误算率是 0.81%）
    > 具体算法可参考：[基数估算（count-distinct problem）](https://wqhuanm.github.io/Issue_Blog/2025/04/14/31_%E5%9F%BA%E6%95%B0%E4%BC%B0%E7%AE%97%EF%BC%88count-distinct.problem%EF%BC%89/)

    + 一个键占用12kb（64位，前14位划分桶，每个桶需要6bit（2^6>50）计算桶value, 合计占用 (2^14 B) *6bit =12kb）

