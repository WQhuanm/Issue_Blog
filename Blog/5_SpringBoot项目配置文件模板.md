---
title: SpringBoot项目配置文件模板
date: 2025-01-26 15:27:32
mathjax: true
categories: 
    - Web后端
tags: 
    - Spring
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202502172200203.jpeg
---

### 版本要求
1. jdk17
2. springboot:3.2.12
3. Maven:3.6.3以上

### 配置文件
#### 1. pom.xml
``` xml
    <!--        spring-boot-starter-parent声明了spring boot的各个依赖及其版本。子项目直接继承它-->
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.12</version>
    </parent>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <!--        启动热部署-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
        </dependency>
        <!--aop 切面-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-aop</artifactId>
        </dependency>
        <!-- AspectJ -->
        <dependency>
            <groupId>org.aspectj</groupId>
            <artifactId>aspectjweaver</artifactId>
        </dependency>
        <!--mysql驱动（8.0.31及之后)-->
        <dependency>
            <groupId>com.mysql</groupId>
            <artifactId>mysql-connector-j</artifactId>
        </dependency>
        <!--mybatisPlus依赖-->
        <dependency>
            <groupId>com.baomidou</groupId>
            <artifactId>mybatis-plus-spring-boot3-starter</artifactId>
            <version>3.5.10.1</version>
        </dependency>
        <!--        redis依赖-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-redis</artifactId>
        </dependency>
        <!--AMQP依赖，包含RabbitMQ-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-amqp</artifactId>
        </dependency>
        <!--连接池依赖-->
        <dependency>
            <groupId>org.apache.commons</groupId>
            <artifactId>commons-pool2</artifactId>
        </dependency>

        <!-- 添加Junit依赖 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <!--lombok-->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
    </dependencies>
```

#### 2. 启动器 Application.java
``` java
@SpringBootApplication
@MapperScan("com.wqhuanm.springbootLearn.mapper")
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

#### 3. application.yml
```yml
server:
  port: 8081
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/wq_learn?characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
    username: root
    password: 123456
    driver-class-name: com.mysql.cj.jdbc.Driver
  data:
    redis:
      host: 192.168.63.130
      port: 6379
      password: 123456
      lettuce:
        pool:
          max-active: 10
          max-idle: 10
          min-idle: 1
          time-between-eviction-runs: 10s
  jackson:
    default-property-inclusion: non_null # JSON处理时忽略非空字段
  rabbitmq:
    host: localhost
    port: 5672
    virtual-host: / #rabbitmq的虚拟主机
    username: admin
    password: 1234
    connection-timeout: 1s # 设置MQ的连接超时时间
    publisher-confirm-type: correlated # 开启publisher confirm机制，类型为异步回调返回
    listener:
      simple:
        prefetch: 5 # 每次只能获取5条消息，处理完成才能获取下一个消息
        acknowledge-mode: auto # 开启消费者确认机制，自动模式
        retry:
          enabled: true # 开启消费者失败重试
          initial-interval: 1000ms # 初始的失败等待时长为1秒
          multiplier: 1 # 失败的等待时长倍数，下次等待时长 = multiplier * last-interval
          max-attempts: 3 # 最大重试次数
          stateless: true # true无状态；false有状态。如果业务中包含事务，这里改为false
mybatis-plus:
  configuration:
    # 日志
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl


logging:
  pattern:
    dateformat: MM-dd HH:mm:ss:SSS #设置日志的日期输出格式
```
