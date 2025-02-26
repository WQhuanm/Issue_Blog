---
title: Java基础知识随记
date: 2025-02-26 08:55:17
categories: 
    - Java
tags: 
    - Java
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202412222015910.png
---

1. Java对象存储在堆中

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

1. Java 集合
    1. ArrayList基于Object[]实现，扩容机制是每次扩容为原来的1.5倍左右
    1. HashSet、LinkedHashSet、TreeSet
        HashSet 的底层数据结构是HashMap。读取顺序是按hash值排序
        LinkedHashSet 的底层数据结构是LinkedHashMap，链表维护元素的插入顺序，能按照添加顺序遍历输出
        TreeSet 的底层数据结构是红黑树
    1. HashMap
        1. HashMap 由 数组+链表/红黑树 组成的（链表长>7且数组长度>63，转换为红黑树）
        总是使用 2 的幂作为哈希表的大小。HashMap 默认的初始化大小为 16。之后每次扩充，容量变为原来的 2 倍。
        1. HashMap 通过 key 的 hashCode 经过扰动函数处理过后得到 hash 值，然后通过 (n - 1) & hash 判断当前元素存放的位置 
        如果当前位置存在元素的话，就判断该元素与要存入的元素的 hash 值以及 key 是否相同，如果相同的话，直接覆盖；不相同就遍历链表插入链表尾部。
        1. loadFactor 负载因子控制数组存放数据的疏密程度。越趋近于 1，那么 数组越密，会让链表的长度增加；越趋近于 0，数组越稀疏。
            + 默认负载因子为0.75f。当元素超过了 n*loadFactor就需要将n进行扩容。
            + 扩容需要重新 hash 分配，并且会遍历 hash 表中所有的元素，非常耗时。
        1. LinkedHashMap 继承自 HashMap，并在 HashMap 基础上维护一条双向链表，支持遍历时会按照插入顺序有序进行迭代。
        1. ConcurrentHashMap线程安全（Synchronized 锁加 CAS 的机制），底层是数组+链表/红黑树




    
