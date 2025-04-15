---
title: 基数估算（count-distinct problem）
date: 2025-04-15 07:14:09
mathjax: true
categories: 
    - CS基础
tags: 
    - CS基础
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202504151511118.png
---

>计算基数（集合中不重复元素的个数，distinct count），在UV统计等大数据量计数操作很常见
一般的精准计数采用hash扰乱+bitmap标记，空间np复杂度为bitmap需要多少位，消耗太大了，因此诞生了基于概率的粗略估计

### Linear Counting（LC算法）
1. 基本思想还是基于bitmap（设映射空间为m，m大约为基数n的十分之一）
1. 元素映射后，设有u个bit为0，则估计基数为 $\hat{n } =-m log\frac{u}{m}$ 
    + 证明可参考[如何科学的计数？](https://bindog.github.io/blog/2015/02/14/cardinality-counting/#linear-counting)

### LogLog Counting(LLC算法)
1. 正如其名，空间复杂度大约只有loglogN（N为基数最值），思想基于伯努利实验
1. 核心实现还是hash把数据映射成数字（一般是64位整数），记低位到高位第一个bit为1是p位，所有插入数字得到的最值p为 $p_{max}$ ，则估计基数为 $2^{ p_{max} }$ 。证明如下
    + 由于hash随机，每个bit位为0，1是独立的。若插入n个数， $p_{max}$ 为k，则第k位出现第一个1的概率是 $2^{-k}$
        + 事件A：进行n次试验，每次p都不大于k， $P(A)={(1-\frac{1}{2^k})}^n$ ,当 n >> 2^k 时 (n远大于2^k)，概率趋近0
        + 事件B：进行n次试验，至少一次p大于等于k， $P(B)=1-P(A)$ ,当 n << 2^k 时，概率趋近0
    + 如果多次实验后，最大为k，可以说明估算基数约为2^k
    + 一般还会把前m位用来划分2^m个桶，把所有桶的p进行均值计算，最终估算基数为 $\hat{n} =\phi \cdot  m \cdot  2^{ \frac{1}{m} \sum_{i=0}^{m-1}p_i }$ （一个桶估计的数量*总共m个桶 ，再乘以调参）
    + 记录p值需要bit为loglogn，m个桶则空间复杂度为m*loglogn
1. 存在问题：离群值对于求和平均影响大

### HyperLogLog（HLL算法）
基于LLC改进
+ 使用调和平均数 $\frac{n}{\sum_{i=1}^{n}\frac{1}{x_i}}  $代替求和平均以减少离群值的影响
+ 但n较小时（有许多桶是空的），采用LC算法



### 参考文章
[如何科学的计数？](https://bindog.github.io/blog/2015/02/14/cardinality-counting/#linear-counting)
[HyperLogLog 算法详解](https://zhuanlan.zhihu.com/p/77289303)


