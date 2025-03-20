---
title: Java基础知识随记
date: 2025-02-26 08:55:17
categories: 
    - Java
tags: 
    - Java
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202502261916407.png
---


### 1. 基础知识
1. Java访问修饰符为默认(default)是包级访问权限，只有包内的类才能访问，而不是public

1. Java只有值传递，不存在C++的引用传递
==比较值（基本类型的值是value，类的值是地址）,equal的比较一般是内容相等（但是Object的equal是=比较）

1. hashCode()用于快速判断元素之间相等，减少equla调用。hash相等才用equal判断是否真相等而非hash冲突。
重写 equals() 时必须重写 hashCode() 方法

1. String、StringBuffer、StringBuilder
    ![](https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202502241948581.png) 
    1. String的值是final，不可变，对其修改/拼接等操作是new String()给他指向
    1. String.intern()：如果常量池中已经存在相同内容的字符串，则返回常量池中已有对象的引用；否则，将该字符串添加到常量池并返回其引用。
    
1. 异常(Exception) :程序本身可以处理的异常，可以通过 catch 来进行捕获。
    1. 分为 Checked Exception (受检查异常，必须处理) 和 Unchecked Exception (不受检查异常，即使不处理不受检查异常也可以正常通过编译)。
    1. 除了RuntimeException及其子类以外，其他的Exception类及其子类都属于受检查异常 。如IO异常

### 2. Java 集合
1. 数组和链表的区别
    + 数组访问速度快，但插入删除慢，且内存必须连续，可能存在空间浪费或不足无法扩展
    + 链表插入速度快，可以动态开辟空间，适合频繁增删改，但是访问速度慢（内存分配、垃圾回收等无需随机访问的经常使用）
    + 循环链表的应用：循环队列（体现公平性、轮询）
1. ArrayList基于Object[]实现，扩容机制是每次扩容为原来的1.5倍左右
1. HashSet、LinkedHashSet、TreeSet
    HashSet 的底层数据结构是HashMap。读取顺序是按hash值排序
    LinkedHashSet 的底层数据结构是LinkedHashMap，链表维护元素的插入顺序，能按照添加顺序遍历输出
    TreeSet 的底层数据结构是红黑树
1. HashMap单独坐一桌：
    1. 由数组+链表/红黑树 组成的（链表长>7且数组长度>63，转换为红黑树）。
        + 元素是Node<K,V>,红黑树的结点TreeNode继承自Node，使得可以用迭代器遍历map所有结点
        + 扩容后，会对链表/红黑树的拆分，根据他们二进制高位（扩容新增那一位）是否为1，会分成2条链表（各自存放到新的map位置），链表长度过长则直接树化
    1. 总是使用 2 的幂作为哈希表的大小。HashMap 默认的初始化大小为 16。之后每次扩充，容量变为原来的 2 倍。
    1. hash()：
        + (h = key.hashCode()) ^ (h >>> 16)，右移一半来异或得到hash值
        + 通过 (n - 1) & hash 判断当前元素存放的位置
        + 如果当前位置存在元素的话，就判断该元素与要存入的元素的 hash 值以及 key 是否相同，如果相同的话，直接覆盖；不相同就遍历链表插入链表尾部。
        + jdk8引入了红黑树，不再有rehash操作来保证扩容后hash的随机性
    1. 核心字段：initialCapacity(初始容量)、loadFactor(负载因子(可以大于1))、threshold（扩容阈值）
        + 扩容阈值一般等于Capacity*loadFactor，如果不超过最大阈值的话。当map元素数量>threshold，执行resize()扩容
        + loadFactor 负载因子控制数组存放数据的疏密程度，默认负载因子为0.75f。
    1. 线程不安全存在的一些问题：
        + 扩容会死循环/死锁（JDK7）：因为采用头插法，导致链表成为环形链表
            ![](https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202503141622646.png)
        + 并发下put元素消失
        + get，put并发导致get为null，因为put导致扩容改位置了
1. 其他Map
    1. LinkedHashMap 继承自 HashMap，并在 HashMap 基础上维护一条双向链表，支持遍历时会按照插入顺序有序进行迭代。
    1. ConcurrentHashMap线程安全（Synchronized 锁加 CAS 的机制），底层是数组+链表/红黑树

### 3.设计模式
1. 单例模式（确保一个类只有一个实例）
    + 双重检验锁方式实现
    ```java
        public class A {
            private volatile static A uniqueInstance;//全局唯一实例，用volatile修饰，保证线程安全
            private A() {}
            public  static A getUniqueInstance() {//获取实例
                if (uniqueInstance == null) {//先判断对象是否已经实例过，没有实例化过才进入加锁代码
                    synchronized (Singleton.class) {//类对象加锁
                        if (uniqueInstance == null) {
                            uniqueInstance = new A();
                        }
                    }
                }
                return uniqueInstance;
            }
        }
    ```
    + uniqueInstance = new Singleton(); 这段代码其实是分为三步执行：
        1. 为 uniqueInstance 分配内存空间
        1. 初始化uniqueInstance；
        1. 将 uniqueInstance 指向分配的内存地址
    + 如果不用volatile修饰，执行顺序可能变为1->3->2，那么其他线程获取实例时可能获取一个没有初始化的null实例


1. 代理模式
    1. 静态代理：在编译时便将代理类变成class文件（一般需要手动增加代理类，除非使用aspectJ）
    1. 动态代理：运行时，代理类无需编译，直接生成代理类的字节码。无侵入性，无需修改目标类源码。
        + JDK动态代理：通过反射机制动态生成代理类（如 Proxy.newProxyInstance()）。只能代理实现了接口的类
        + CGLIB动态代理：通过字节码生成库（如 ASM）动态创建目标类的子类。只能代理public且**非final**的方法/类


    

