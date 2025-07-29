---
title: Junit 单元测试
date: 2025-06-17 03:59:23
mathjax: true
categories: 
    - Web后端
tags: 
    - Java
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202506292029993.png
---

### JUnit4
#### 常用注解
+ @Test：声明为测试方法，方法要求为**public void**且**throws Exception**
+ @BeforeClass/@AfterClass：在调用该类的测试方法前/后，统一执行一次
+ @Before/@After：在调用每个测试方法前/后，都会执行一次


#### @RunWith(xxx.class)：声明该测试类的运行器为xxx，未显式声明则使用默认
+ Parameterized.class：参数运行器，配合@Parameters使用junit的参数化测试功能
    + 把被测试函数需要使用的参数及其输出，作为类的变量，并设置相应的构造函数
    + 使用@Parameters注解的方法（要求是public static Collection<Object[]>）来注入测试参数
        + 每个Object[]就是一组数据，元素顺序保持与构造函数一致
    ```java
        @RunWith(Parameterized.class)
        public class MyTest
        {
            private int val1;
            private String val2;
            private String expected;
            private UserService userService = new UserServiceImpl();
            
            public MyTest(int val1, String val2, String expected)
            {
                this.val1 = val1;
                this.val2 = val2;
                this.expected = expected;
            }

            @Parameterized.Parameters
            public static Collection<Object[]> data()
            {
                List<Object[]> arr = new ArrayList<Object[]>();
                arr.add(new Object[]{123,"345abc","wqwq"});
                return arr;
            }

            @Test
            public  void test() throws Exception
            {
                String res = userService.getUserName(val1,val2);
                assertEquals(expected, res);
            }
        }
    ```

+ Suite.class：套件测试，用于一次运行多个测试类
    + 定义一个空类，使用@Suite.SuiteClasses需要运行的测试类注入
    ```java
    @RunWith(Suite.class)
    @Suite.SuiteClasses({
            Test1.class,
            Test2.class
    })
    public class MyTest {
    }
    ```

+ Enclosed.class：嵌套测试，一个空的外部测试类，内部可以定义多个测试类
    + 内部测试类必须是public static class
    ``` java
    @RunWith(Enclosed.class)
    public class MyTest
    {
        public static class Test1{
            @Test
            public  void test() throws Exception{
            }
        }
        public static class Test2{
            @Test
            public  void test() throws Exception{
            }
        }
    }
    ```






### JUnit 5 参数化测试核心注解
#### 常用注解
+ @BeforeAll/@AfterAll：在调用该类的测试方法前/后，统一执行一次
+ @BeforeEach/@AfterEach：在调用每个测试方法前/后，都会执行一次

#### 参数化测试：@ParameterizedTest
##### 参数提供注解
+ @ValueSource: 提供单个参数（参数需是原始类型）  

    ```java
    @ParameterizedTest
    @ValueSource(longs = {233,666})
    public void test() throws Exception{
    }
    ```

+ @CsvSource: 提供多个参数（参数需是原始类型）
    + 每组数据用一个字符串表示，字符串中的元素用逗号分隔,存在不提供的值，也需要隔开
    ```java
    @ParameterizedTest
    @CsvSource(value = {"arg1, 1 ,val1", "arg2,,val2"})
    public void test(String arg, Integer value,String val) throws Exception{
    }
    ```

+ @CsvFileSource: 同上一个注解，但数据从csv文件读取：@CsvFileSource(resources = "/data.csv")

+ @MethodSource: 从一个无参静态方法中获取 `Stream` 或 `Collection` 作为多组参数（参数类型无限制）

    ```java
    @ParameterizedTest
    @MethodSource("getParams")
    public void test(User user, int time) throws Exception{
    }

    private static Stream<Arguments> getParams() {//无参静态方法提供参数
        return Stream.of(
                // 有效用户和时间
                Arguments.of(new User("Alice"), 123),
                Arguments.of(new User("Bob"), 456)
        );
    }
    ```

### 参考文章
[单元测试 - JUnit4 详解](https://www.pdai.tech/md/develop/ut/dev-ut-x-junit.html#%E6%B5%8B%E8%AF%95-%E5%8F%82%E6%95%B0%E5%8C%96%E6%B5%8B%E8%AF%95)  
[JUnit 5参数化方法测试（一）](https://zhuanlan.zhihu.com/p/262508766)  
[JUnit 5 用户指南](https://junit.java.net.cn/junit5/docs/current/user-guide/#overview)  
