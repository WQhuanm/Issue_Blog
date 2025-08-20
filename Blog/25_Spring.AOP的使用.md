---
title: Spring AOP的使用
date: 2025-04-01 08:12:40
mathjax: true
categories: 
    - Web后端
tags: 
    - Spring
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202502172200203.jpeg
---


### 一，AOP基础概念
1. 连接点（Join Point）：可以认为ioc容器的所有类（不包括切面类）的所有**方法执行（运行时的方法）**都是JoinPoint，他们都能被增强
1. 切点（Poincut）：定义了切入哪些连接点，即增强哪些方法（通过表达式或注解声明这些方法）
1. 通知（Advice）：定义了如何切入（before，after，around...）
1. 切面（Aspect）：由@Aspect定义的类即为切面类，切面类声明了如何用切点和通知来增强连接点
1. 织入（Weaving）：AOP的创建代理对象的方式（编译期织入、类加载期织入、运行期织入）

### 二，AOP的使用
#### 1. aop环境配置
1. pom.xml

    ```xml
            <!--aop 切面-->
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-starter-aop</artifactId>
            </dependency>
    ```
1. Application启动类开启注解

    ```java
    @EnableAspectJAutoProxy(exposeProxy = true)//启用AOP自动代理，允许暴露代理类
    ```

#### 2. 切面的声明
> 基本步骤就是声明为切面类，定义切点表达式，编写advice通知方法

1. 切点表达式（指明增强的方法）
    1. execution表达式
        + execution(* com.wqhuanm..*.*(..)) 任意返回类型，com.wqhuanm的包及其子包，任意类 ，任意方法 ，(..)任意参数
        + execution(public int com.wqhuanm.MyserviceImpl.*(String name, ..)) public且返回为int，指定类的任意第一个参数为string的方法
    1. @annotation注解

        ```java
            @Pointcut("@annotation(com.learn.annotation.SystemLog)")//增强使用了这个注解的方法
            public void pt() {
            }

            @Target({ElementType.METHOD})
            @Retention(RetentionPolicy.RUNTIME)
            public @interface SystemLog {
                String BusinessName();// 接口调用该注解时，声明其相应功能,如@SystemLog(BusinessName = "更新个人信息")
            }
        ```
1. 连接点JoinPoint
    + JoinPoint：用于获取目标对象/代理对象/方法签名/参数
    + ProceedingJoinPoint：JoinPoint的子接口，提供proceed()：执行目标方法

1. advice通知写法

    ```java
    @Aspect//声明为切面类
    @Component
    public class LogAspect {
        @Pointcut("execution(* com.wqhuanm.learn..*.*(..))")
        public void logPt(){}//函数名用于声明该切点的名字
        
        @Before("logPt()")
        public void beforePrint(JoinPoint jp){
            System.out.println("before print:  "+jp.getSignature().getName());
        }

        @Around("logPt()")
        public void aroudPrint(ProceedingJoinPoint jp){
            Object ans=null;
            System.out.println("Before");
            try {
                ans= jp.proceed();
                System.out.println("AfterReturning");
            } catch (Throwable e) {
                System.out.println(e.getMessage());
                System.out.println("AfterThrowing");
            }finally {
                System.out.println("After");
            }
        }
    }
    ```




### 三，多个AOP的执行顺序
1. AOP的优先级由他们的order值决定，order值越低，优先级越高。spring aop（包括事务）的优先级默认都是Integer.MAX_VALUE（即优先级最低）
1. 如果切面间优先级相同，则由他们注册到Spring的顺序决定谁优先级高（越先注册越高），事务之类的基础设施切面的注册往往早于自定义切面的注册时机
1. 多个切面可以看成是以方法执行为圆心，优先级越高的切面在外环，越低的在内环。而切面的执行可看成一个箭头穿过圆环得到的顺序（优先级越高，越先开始，但是越晚结束）
    ![](https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202504021928189.png)
1. 优先级的定义
    + 自定义切面可以在切面类上注解@Order(value)来设定order值（直接作用于方法上无效）
    + Spring的事务优先级可在启动类上设置@EnableTransactionManagement(order = value)来设置order值

1. 事务与自定义切面同时使用可能存在的问题
    1. 在均为设定优先级时，事务切面比自定义切面早注册，在外环
    1. 如果事务内容抛出异常，会先被自定义切面捕获，如果切面处理异常后没有把异常抛出，则事务切面接受不到异常，不会执行回滚
    1. 解决思路
        + 要么提高自定义切面优先级，让事务处理后再到切面catch异常
        + 要么自定义切面要抛出异常

### 附录：使用AspectJ
只需引入下面依赖
```xml
<!-- AspectJ -->
<dependency>
    <groupId>org.aspectj</groupId>
    <artifactId>aspectjweaver</artifactId>
</dependency>
```

### 参考文章
[彻底征服 Spring AOP 之 理论篇](https://segmentfault.com/a/1190000007469968#item-1-2)  