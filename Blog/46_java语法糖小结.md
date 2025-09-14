---
title: java语法糖小结
date: 2025-08-25 09:21:18
mathjax: true
categories: 
    - CS基础
tags: 
    - Java
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202509141040515.jpg
---


1. 函数式编程
    - 函数式接口 ：Function<T,R>
        - 只包含一个抽象方法：R apply(T t)，表示接受一个参数T并产生一个结果R的函数
        - 通过传递该接口的实现类，就能传递一个函数
    - Lambda表达式 ：([params]) -> {} ，该表达式可以用于实现函数式接口（快速定义一个函数并作为参数传递）
    - 方法引用(obj::methodName, class::staticMethodName) 
        - 如果是传递一个类/实例的方法，可以使用方法引用作为简写的lambda表达式（等价于(T t)->{return t.method};

1. Preconditions类 ：提供的静态方法用于check变量(com.google.common.base.Preconditions)
    - checkArgument(boolean, [err_string]) ：用于检测方法参数是否满足布尔表达式，不满足会抛出异常
    - checkState(boolean, [err_string]) ：用于检测对象是否满足布尔表达式，不满足会抛出异常
    - checkNotNull(obj, [err_string]) ：用于检测对象是否非null，不满足会抛出异常

1. Optional<T> ：用于判空处理(java.util.Optional)
    - Optional.ofNullable(obj) ：传入obj并封装为Optional<obj>, 如果obj为null，则获得一个空的Optional
    - Optional.map( Function<T,U> ) ：以函数作为参数（其中函数的参数是Optional封装的类T），如果Optional不是空对象，则会调用该方法，并把结果封装为Optional\<U>，否则返回一个空Optional
    - Optional.flatmap( Function<T,Optional\<U>> ) ：如果当前Optional不是空对象，则会调用该方法(要求方法返回值是Optional),因为不会再对结果进行Optional封装
    - Optional.orElse(T) ：获取Optional封装的对象，如果是空对象，则使用传入的参数作为返回值
