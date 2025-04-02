---
title: Spring学习笔记
date: 2025-03-20 10:47:09
categories: 
    - SpringBoot
tags: 
    - SpringBoot
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202502172200203.jpeg
---

### Spring
#### 1.IOC（Inversion of Control:控制反转）
##### 1.定义
1. 将对象创建（实例化、管理）的权力（控制权）交给Spring的IOC容器（反转）
1. 优点
    + 不再需要考虑一个类依赖其他类时要如何考虑依赖类的构造函数，只需要向IOC容器申请这个依赖类的实例即可
    + 对象之间的耦合度/依赖程度降低
##### 2.依赖注入（DI,Dependency Injection）(IOC思想的具体实现)
1. Bean的3种注入方式
    + 构造函数注入：通过类的构造函数来注入依赖项（推荐，确保对象实例化时就注入，避免初始化时还未注入，属性却被引用导致空指针）
    + Setter 注入：通过类的 Setter 方法来注入依赖项
    + Field（字段） 注入：直接在类的字段上使用注解（如 @Autowired 或 @Resource）来注入依赖项

1. @Autowired 和 @Resource 的区别
    + @Autowired 是 Spring 提供的注解，@Resource 是 JDK 提供的注解。
    + @Autowired：默认使用 byType（根据接口去寻找实现类），如果接口有多个实现类，使用byName（根据名称进行匹配）
    + @Resource：默认使用byName。无法名称匹配到Bean则注入方式会变为byType。
##### 3.Bean
1. Bean 的作用域
    + singleton（默认）: IoC 容器中只有唯一的 bean 实例
    + prototype : 每次获取都会创建一个新的 bean 实例
    + request: 每次 HTTP 请求都会产生一个新的bean
    + session : 每次session请求都会产生一个新的 bean
    + websocket：每次 WebSocket 会话产生一个新的 bean。
    + application/global-session：每个 Web 应用在启动时创建一个 Bean（应用 Bean），该 bean 仅在当前应用启动时间内有效。

1. Bean 的生命周期
    1. 创建Bean实例：Bean容器首先会找到配置文件中的Bean定义，然后使用 Java 反射 API 来创建 Bean 的实例
    1. Bean 属性赋值/填充：为 Bean 设置相关属性和依赖注入
    1. Bean 初始化（对Bean实现的一些初始化接口进行调用）
    1. 销毁 Bean：把 Bean 的销毁方法先记录下来，将来需要销毁 Bean 或者销毁容器的时候，就调用这些方法去释放 Bean 所持有的资源。

#### 2.AOP（Aspect oriented programming:面向切面编程）
> AOP的使用可以参考[Spring AOP的使用](https://wqhuanm.github.io/Issue_Blog/2025/04/01/25_Spring.AOP%E7%9A%84%E4%BD%BF%E7%94%A8/)
1. spring AOP的实现
    + Spring AOP基于动态代理，低版本spring默认jdk代理，高版本默认CGLIB代理（JDK动态代理可能导致类型转换异常），没有专门导入AspecJ则使用的是Spring AOP。动态代理方式无侵入性，无需修改目标类。（Spring AOP只能拦截ioc容器里面的对象）
    + AspectJ AOP（编译时/类加载时增强，静态代理，字节码织入），运行时无代理开销，性能更高，但是在编译时修改目标类字节码，存在侵入性
    + 基于CGLIB生成代理子类proxy例子如下：
        ``` java
        public UserService$$EnhancerBySpringCGLIB extends UserService {//CGLIB生成的代理类
            UserService target;//目标类
            MyAspect aspect;//@Aspect修饰的切面类（定义了如何增强目标类）

            public UserService$$EnhancerBySpringCGLIB() {
                //此处未使用super()方法
            }

            public ZoneId getZoneId() {
                aspect.doAccessCheck();
                return target.getZoneId();
            }
        } 

        @Component//目标类
        public class UserService {
            // 成员变量:
            public final ZoneId zoneId = ZoneId.systemDefault();
            // 构造方法:
            public UserService() {
            }
            // public方法:
            public ZoneId getZoneId() {
                return zoneId;
            }
            // public final方法:
            public final ZoneId getFinalZoneId() {
                return zoneId;
            }
        }  

        @Aspect
        @Component
        public class MyAspect {
            @Before("execution(public * com..*.UserService.*(..))")
            public void doAccessCheck() {
                System.err.println("[Before] do access check...");
            }
        }
        ```
    + 一些细节问题如下
        1. proxy代理的原理是重写，在目标方法周围增加增强的逻辑，而目标方法的使用是直接调用目标方法去执行
        1. proxy无法代理目标类的final方法，因为代理的本质是重写
        1. proxy的构造函数不会调用super(),也不会初始化成员变量
            1. 因为没必要，proxy的目标是代理方法，且原本方法的执行也是目标类去执行
                + 只有原始Bean会执行原始方法，修改原始字段
                + 因此代理类操作成员变量都需要通过方法(getter/setter)
            1. 经过编译器编译后的代码实际构造函数组成是
                1. super();
                1. 父类所有显式初始化的变量在构造函数初始化（即上图UserService成员变量在定义时直接赋值，即为显式初始化）
                1. 原本构造函数的初始化内容
                + 动态代理不经过编译器修饰，是不会有前面添加的2步的，所以成员变量都是null
                
    + Spring可以通过 AopContext.currentProxy()获取代理对象(前提是当前对象有被开启AOP代理，启动类要允许获取代理对象：@EnableAspectJAutoProxy(exposeProxy = true))
1. AOP的通知类型
    + Before
    + After
    + Returning（返回通知）：目标对象的方法调用完成，在返回结果值之后触发
    + AfterThrowing（异常通知）：目标对象的方法运行中抛出 / 触发异常后触发
    + Around （环绕通知）

1. Spring AOP的一些问题
    + this自调用问题(动态代理本身的问题)：this调用会直接指向目标对象本身，而不经过代理对象。因此，代理的拦截逻辑不会生效。

#### 3. 事务(@Transactional（声明式事务，相较于编程式事务更简洁）)
1. 事务传播行为
    + TransactionDefinition.PROPAGATION_REQUIRED（默认）：如果当前存在事务，则加入该事务；如果当前没有事务，则创建一个新的事务。
    + TransactionDefinition.PROPAGATION_REQUIRES_NEW：创建一个新的事务，如果当前存在事务，则把当前事务挂起。（内部事务提交或回滚不影响外部事务。）
    + TransactionDefinition.PROPAGATION_NESTED：如果当前存在事务，则创建一个事务作为当前事务的嵌套事务来运行（内部事务异常默认会传播到外部事务，导致整体回滚。）
1. 回滚策略（spring 的事务只能对数据库等支持回滚操作的数据进行回滚，其他数据不行）
    + 默认回滚策略是只有在遇到RuntimeException / Error时才会回滚事务，而不会回滚 Checked Exception（受检查异常）
    + 可以使用@Transactional 注解的 rollbackFor 和 noRollbackFor 属性来指定
    + 声明式事务部分回滚的策略（支付金额回滚，支付记录（成功/失败）不回滚）
        1. 可以把事务拆分成多个子事务，传播策略是挂起当前事务，则大事务的回滚不会使得部分小事务必须跟着回滚
        1. 在事务方法内部手动捕获异常处理后手动代码回滚（TransactionAspectSupport.currentTransactionStatus().setRollbackOnly();），不把异常抛出让事务切面回滚。回滚逻辑由我们定义，可以实现异常与否时执行不同逻辑
        1. 自定义aop切面，优先级低于事务，他会比事务切面提前获得异常，自定义切面来处理异常，不抛出给事务切面回滚

1. 事务失效的可能
    + 因为事务基于AOP，this调用等AOP错误会导致事务失效
    + 抛出的异常被提前捕获处理掉，没有被事务切面接受到
    + 数据不支持回滚


#### 4.Spring MVC（模型(Model)、视图(View)、控制器(Controller)）
1. MVC模式
    ![](https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202503201159510.png)
    1. 客户端（浏览器）发送请求， DispatcherServlet拦截请求
    1. DispatcherServlet 根据请求信息调用 HandlerMapping（根据URL去匹配查找能处理的Handler（即Controller），并会将请求涉及到的拦截器和 Handler 一起封装
    1. DispatcherServlet 调用 HandlerAdapter适配器执行 Handler 。Handler执行后返回一个 ModelAndView 对象给DispatcherServlet
    1. ViewResolver 会根据逻辑 View 查找实际的 View（视图渲染）。
    1. DispaterServlet 把返回的 Model 传给 View（视图渲染）。
    1. 把 View 返回给请求者（浏览器）

1. 过滤器（Filter）和拦截器（Interceptor）的区别
    ![](https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202503201311670.png)
    + Filter基于servlet，基于方法回调实现（决定是否把资源释放给下一个filter
    + Interceptor基于Spring，基于动态代理实现

#### 5.Spring的启动流程
1. 创建IOC容器：ApplicationContext对象
1. 读取和解析配置文件(XML文件、注解配置类等),将解析到的符合注册条件的Bean转换为BeanDefinition对象，并注册到BeanFactory（默认接口实现类是：DefaultListableBeanFactory）
1. Spring容器刷新（refresh(),核心步骤）
    1. 获取BeanFactory并完成对所有BeanDefinition的解析和注册
    1. 注册Bean后处理器（BeanPostProcessor）。这些处理器允许在Bean初始化前后进行拦截处理（如AOP代理、依赖注入后的处理等）
    1. 实例化单例非懒加载Bean（即注册Bean，调用构造方法创建；多实例Bean按需创建）
    1. 初始化Bean（依赖注入，执行定义的初始化方法）
    1. 初始化事件广播器（用于处理应用事件）和事件监听器（监听Spring容器发布的事件）

### SpringBoot（约定大于配置）
1. @SpringBootApplication注解（主要由3个注解组成）
    + @EnableAutoConfiguration：启用 SpringBoot 的自动配置机制
    + @ComponentScan： 扫描被注解的 bean，注解默认会扫描该类所在的包下所有的类。
    + @Configuration：允许在上下文中注册额外的 bean 或导入其他配置类

1. 自动配置原理
    1. 步骤
        1. 收集自动配置类：启动时，从当前包和所有的 starter 的 resource/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports 文件（旧版本是META-INF/spring.factories）中读取所有的自动配置类，并通过 @Import 导入这些类。
        1. 条件检查：根据 @Conditional 注解进行条件检查，确保只有符合条件的自动配置类才会被加载到 IoC 容器中
        1. 注入所需的 Bean
    1. Spring Boot 自动配置与 Spring 自动装配的区别
        + Spring 自动装配：指通过 @Autowired 等注解，根据类型自动注入依赖 Bean。它侧重于注入已经配置好的 Bean。
        + Spring Boot 自动配置：是根据类路径中的依赖和环境信息自动配置 Spring 组件的过程。它负责创建并配置所需的基础设施 Bean。

1. Spring-Starter实现
    1. 创建starter工程，导入必要依赖
        ![](https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202503201838715.png)
        ``` xml
        //定义了该包install后的starter名字/组别/版本
        <groupId>org.learn</groupId>
        <artifactId>example-spring-boot-starter</artifactId>
        <version>1.0-SNAPSHOT</version>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-autoconfigure</artifactId>
        </dependency>
        ```
    1. 编写自动配置类和业务类
        ``` java
        @Configuration//定义自动配置类
        public class AutoConfiguration {
            @Bean //在配置类注入我们实现的bean
            public MyExample myExample(){
                return new MyExample();
            }
        }

        public class MyExample {//实现的业务类
            public void print(){
                System.out.println("这是starter");
            }
        }
        ```
    1. 在resource/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports下配置我们的配置类的全类名
        ``` imports
        com.example.AutoConfiguration
        ```
    1. meavn install后即可本地导入该stater

1. @PathVariable 和 @RequestParam 和@RequestBody
    + @PathVariable用于获取路径参数，@RequestParam用于获取查询参数。
    + @RequestBody读取请求body的json内容
    ```java
    @GetMapping("/klasses/{klassId}/teachers")
    public List<Teacher> getKlassRelatedTeachers(
            @PathVariable("klassId") Long klassId,
            @RequestParam(value = "type", required = false) String type ) {
    }
    //请求的 url 是：/klasses/123456/teachers?type=web   ，获取数据：klassId=123456,type=web
    ```

    



