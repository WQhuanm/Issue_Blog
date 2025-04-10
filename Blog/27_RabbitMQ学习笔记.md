---
title: RabbitMQ学习笔记
date: 2025-04-10 03:15:19
categories: 
    - 开发中间件
tags: 
    - 开发中间件
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202504101114379.png
---

### 基础知识
1. 基本架构
  ![](https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202504081037555.png)
  ![](https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202504101051992.png)
  + **Broker**：即RabbitMQ的实体服务器。提供一种传输服务，维护一条从生产者到消费者的传输线路，保证消息数据能按照指定的方式传输。
  + **exchange**：交换机，负责消息路由。
  + **virtual host**：虚拟主机，起到数据隔离的作用。每个虚拟主机相互独立，有各自的exchange、queue
  + **Channel**：建立在tcp上的虚拟消息通道，也称信道。每个tcp连接可建立多个Channel（类似http2的流），每个Channel代表一个会话任务
1. 交换机类型
  + Fanout：广播，将消息交给所有绑定到交换机的队列
  + Direct：订阅，基于RoutingKey（路由key）发送给订阅了消息的队列
  + Topic：通配符订阅，与Direct类似，只不过多个RoutingKey用.隔开，且可以使用通配符（#匹配0或多个key，*匹配一个key，eg：china.new.#.haha，#表示中间可以有其他key）
  + Headers：头匹配，基于MQ的消息头匹配，用的较少

1. MQ可靠性保证
  1. 生产者确认机制：Publisher Confirm机制（消息入队成功则返回ack，否则返回nack）
  1. MQ可靠性
    + 默认开启数据持久化（ps：消息持久化后才会返回给生产者ack）
    + 默认开启LazyQueue：接收到消息直接存入磁盘，消费时才从磁盘读取到内存（懒加载）
  1. 消费者保证
    1. 消费者确认机制
      + **manual**：手动模式。需要调用api发送ack或reject
      + **auto**：自动模式。基于aop，当业务正常执行时则自动返回ack；业务异常自动返回nack；消息处理或校验异常自动返回reject;
    1. 消费者重试机制：开启后，失败会再本地重试，重试达到最大次数后执行失败处理策略
  1. 失败处理策略
    + ImmediateRequeueMessageRecoverer：重试耗尽后，返回nack，消息重新入队
    + RepublishMessageRecoverer：重试耗尽后，将失败消息投递到指定的交换机（死信队列）


1. 延迟队列（需要使用插件，即声明交换机为延迟交换机）
  ```java
    @RabbitListener(bindings = @QueueBinding(
            value = @Queue(name="delay.queue"),
            exchange = @Exchange(name = "delay.ec",type = ExchangeTypes.DIRECT,delayed = "true"), //设置为delay队列
            key="delay"
    ))
    public void listenDelay(User user){
        System.out.println("消费者4接收到direct.queue的消息："+ user );
    }

    rabbitTemplate.convertAndSend(delayExchange,key,user,message -> {
                message.getMessageProperties().setHeader("x-delay",5000);//消息头设置延迟时间
                return message;
            });  
  ```


### SpringAMQP的编写方式
1. 注解配置消费者对应的队列和交换机
  ```java
    @RabbitListener(bindings = @QueueBinding( //配置该消费者对应的队列和交换机以及队列订阅的key
            value = @Queue(name = "direct.queue"),
            exchange = @Exchange(name = "direct.exchange", type = ExchangeTypes.DIRECT),
            key = {"red", "blue"}
    ))
    public void listenDirectQueue1(String msg){
        System.out.println("消费者1接收到direct.queue的消息：【" + msg + "】");
    }

    @RabbitListener(bindings = @QueueBinding(
            value = @Queue(name = "topic.queue"),
            exchange = @Exchange(name = "topic.exchange", type = ExchangeTypes.TOPIC),
            key = "china.#"
    ))
    public void listenTopicQueue1(String msg){
        System.out.println("消费者1接收到topic.queue的消息：【" + msg + "】");
    }


  //发布者发布格式一般就是指定[交换机],路由key(没有交换机时则队列名字)，消息Object（要定义序列化器，且类要实现了序列化接口Serializable）
  rabbitTemplate.convertAndSend(exchange,key,message);
  ```
1. 定义消息转换器
  ```java
  @Bean
  public MessageConverter messageConverter(){
      // 1.定义消息转换器
      Jackson2JsonMessageConverter jackson2JsonMessageConverter=new Jackson2JsonMessageConverter();
      // 2.配置自动创建消息id，用于识别不同消息，也可以在业务中基于ID判断是否是重复消息
      jackson2JsonMessageConverter.setCreateMessageIds(true);
      return jackson2JsonMessageConverter;
  }
  ```





### 附：RabbitMQ的Docker部署与整合配置
#### Docker部署
1. 基本部署
    ```shell
    docker pull rabbitmq:management
    docker run -d `
      --name rabbitmq `
      -p 5672:5672 `
      -p 15672:15672 `
      -v rabbitmq_data:/var/lib/rabbitmq `
      -e RABBITMQ_DEFAULT_USER=admin `
      -e RABBITMQ_DEFAULT_PASS=1234 `
      rabbitmq:management
    ```
1. 添加DelayExchange延迟消息插件
    + 先下载[插件](https://github.com/rabbitmq/rabbitmq-delayed-message-exchange)
        ```shell
        docker cp rabbitmq_delayed_message_exchange-v4.0.7.ez rabbitmq:/plugins
        docker exec -it rabbitmq rabbitmq-plugins enable rabbitmq_delayed_message_exchange
        ``` 
#### 整合rabbitmq

1. 导入AMQP依赖
  ~~~xml
  <!--AMQP依赖，包含RabbitMQ-->
  <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-amqp</artifactId>
  </dependency>
  ~~~

1. application.yml配置



