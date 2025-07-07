---
title: Spock单元测试
date: 2025-06-29 14:20:03
mathjax: true
categories: 
    - Java
tags: 
    - Java
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202506292029993.png
---


### 基础
1. spock主要通过given、when、then、where标签来执行测试，常用标签如下  
    1. given：构造输入条件
    1. when：被测试函数的调用
    1. then：通过布尔表达式进行断言
    1. where：提供参数化测试，为上文出现的变量赋值
    1. expect: 简单测试，相当于then+where
    1. and：可视为子标签，一般用于补充说明其代码段的含义

1. 生命周期方法：全局定义的字段默认每次运行测试用例都会重新初始化，可以使用@Shared标记字段，则变为共享
    + setup/cleanup 方法：每次运行测试用例执行一次
    + setupSpec/cleanupSpec 方法：全局只执行一次

### Mock & Spy
#### Mock
> 被mock的对象，会记录所以与它进行的交互，用于拦截目标对象方法的调用  
被mock对象的所有方法被调用时，如果没有模拟，则会返回方法返回类型的默认值
只能模拟公共方法，私有方法不可模拟

+ 创建Mock对象时需要传入目标类
+ 用>>模拟方法,右侧是一个闭包（值/方法）
    + 形如 dao.getid(_,_ as String) >> [id1,id2]（这里闭包是数组）
    + 闭包可以是自定义函数(类似lambda)，可以获取方法的参数，如 dao.getid(_,_ as String)>>{int id ,String name -> id == 123}
+ _代表一个任意类型、任意值的参数,也可以使用as指定其类型
+ 若要模拟多次值
    + 可使用多个>>即可，如：dao.getid(_) >> res1 >> res2
    + 或者使用>>>，用数组包裹：dao.getId(_) >>> [ res1 , res2]
+ 交互计数：用于断言方法被调用了多少次
    + 如 2 * dao.getid(_) >> res 判断是否使用2次
    + 0 * _ 表示除了显示计数的方法外，其余方法应该被调用0次

#### Spy
> Spy的对象默认调用方法都使用真实方法，除非方法被模拟，模拟方式同Mock

+ 创建Spy对象时可以传入目标类或者对象

#### 测试类结构示例
```Java
class test extends Specification //使用Spock需要继承的类
{
    def dao = Mock(UserDao)
    def spy = Spy(new UserServiceImpl(userDao: dao)) //groovy可以指定使用哪些字段来构造类

    def "当前测试的username=#name"() { //#，字面值引用，可以把字符串的值替换为引用的变量值
        given: "构造输入条件"
        def stu = new User(userId: id, userName: name)
        def stu2 = new User(userId: id2, userName: "lihua")

        and: "进行Mock/Spy"
        dao.getUser(_) >> stu >> stu2
        spy.allow() >> true

        when: "测试函数的调用"
        def res = spy.getUserById(123)
        def res2 = spy.getUserById(456)

        then: "对测试结果的验证"
        with(res) {//语法糖，内部变量为res的字段
            userId == out_id
            userName == out_name
        }
        res2.userId == 555

        where: "参数化测试"
        //第一行是列名，上面使用过的变量，一般每个列用|隔开，输入输出变量间用||隔开，即左边是输入值，右边是输出值
        id  | id2 | name    || out_id | out_name
        666 | 555 | "lihua" || 666    | "lihua"
        333 | 555 | "aaa"   || 333    | "aaa"
    }
}
```


### 异常测试
> 异常断言: 使用thrown(expectedException)方法来断言when 执行的函数抛出异常是否为thrown的参数预期值，thrown可以捕获异常实例

```java
def "validate student info: #expectedMessage"() {
    when: "执行测试函数"
    tester.validateStudent(student)

    then: "验证，捕获异常"
    def exception = thrown(expectedException)
    exception.code == expectedCode
    exception.message == expectedMessage

    where: "测试数据"
    student           || expectedException | expectedCode | expectedMessage
    getStudent(10001) || Exception1 | "10001"      | "student is null"
    getStudent(10002) || Exception2 | "10002"      | "student name is null"
    getStudent(10003) || Exception3 | "10003"      | "student age is null"
}
```

### Spock的依赖
Spock进行mock和spy时，默认时只能对有接口的类进行，除非引入字节码增强
cglib不支持高版本jdk，可以改为Byte Buddy
``` xml
<!--spock-->
<dependency>
    <groupId>org.spockframework</groupId>
    <artifactId>spock-core</artifactId>
    <version>2.3-groovy-4.0</version>
    <scope>test</scope>
</dependency>
<!--Byte Buddy-->
<dependency>
    <groupId>net.bytebuddy</groupId>
    <artifactId>byte-buddy</artifactId>
    <version>1.14.6</version>
</dependency>
```

### 参考文章
[Spock单元测试框架介绍以及在美团优选的实践](https://tech.meituan.com/2021/08/06/spock-practice-in-meituan.html)  
[字节码增强技术，不止有 Java Proxy、 Cglib 和 Javassist 还有 Byte Buddy](https://cloud.tencent.com/developer/article/2385290)  

