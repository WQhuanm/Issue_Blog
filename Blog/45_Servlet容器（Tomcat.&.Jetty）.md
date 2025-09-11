---
title: Servlet容器（Tomcat & Jetty）
date: 2025-08-25 06:58:40
mathjax: true
categories: 
    - Web后端
tags: 
    - Java
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202412222015910.png
---


![](https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202507270024815.png)

### Servlet
1. servlet的作用 ：web请求的处理，底层通信协议是交给web server（比如http server）来进行。而具体的业务逻辑处理，则是交给servlet
1. servlet接口
    - 最重要的是定义了service方法：要求具体业务类在该方法实现业务逻辑
        - void service(ServletRequest req, ServletResponse res) ：该方法的2个参数是对web请求和响应的封装
        - 上述2个参数都是接口，其http下有子接口HttpServletRequest和HttpServletResponse
        - 可以通过HttpServletRequest，HttpServletResponse分别来创建或获取session，cookie
    - 定义了一个servlet的初始化/销毁/获取配置信息等方法
    - 抽象类GenericServlet实现了servlet接口，抽象类HttpServlet继承了GenericServlet，我们可通过继承HttpServlet类来实现自己的Servlet（重写doGet、doPost方法）
1. servlet容器（web容器）
    - servlet容器是对servlet规范的实现，servlet容器用于加载和管理实现了servlet接口的业务类
    - web server只与servlet容器交互，与具体业务解耦
        - web请求经过web server传递给servlet容器，servl容器将其封装为ServletRequest并寻找合适的servlet去处理
        - servlet处理完请求后，容器会对ServletResponse解封装并传递给web server
    - Filter ：实现了Filter接口的过滤器交由servlet容器管理(过滤器链)，请求和响应都会经过过滤器链处理

### Tomcat
#### 整体架构
1. Tomcat 有两大组件：Connector连接器 和 Container容器
  - Connector ：负责网络通信，即web server职能。一个Connector负责监听处理一个端口的请求
  - Container ：负责处理请求，即servlt容器职能
1. 两个组件的组合逻辑，抽象成了Service服务单元来管理
  - 一个Service可以有多个Connector，每个Connector由唯一的Service管理。
    - 每一个连接器都会在指定的端口上处理Socket链接，采用一种IO模型传输字节流，并使用一种应用层协议进行解析
  - 一个Service管理一个唯一容器：Engine（顶层容器）
1. Tomcat实例（server）又负责管理多个服务单元Service
![](https://cdn.jsdelivr.net/gh/WQhuanm/Img_repo_1/img/20250725101905995.png)

#### 连接器
+ 连接器有三大职能
  - 按照**特定的IO模型**传输字节流 ：EndPoint组件
    - 使用Acceptor组件监听Socket请求，并封装成runnable任务提交到线程池，任务读取字节流后会调用Processor进行解析
  - 按照**应用层协议**实现字节流与TomcatRequest/TomcatResponse的转换 ：Processor组件
  - 按照**Servlet规范**实现TomcatRequest/TomcatResponse与ServletRequest/ServletResponse间的转换 ：Adapter组件 
1. EndPoint与Processor之间的组合逻辑（涉及多种IO模型，应用层模型的组合），又抽象成ProtocolHandler接口来封装

#### Servlet容器（多层容器实现）
##### 多层容器的设计
1. 一个web服务URL 往往可以被划分为5个部分 ：应用层协议(http，https等)，域名/ip，服务端口，域名指定路径上部署的服务，子路径上的具体业务  
  - 如https://wqhuanm.github.io:443/Issue_Blog/2024/12/21/1_About.me ：使用https协议，在wqhuanm.github.io域名的443端口上，路径Issue_Blog提供了一个blog网站服务，该服务的子路径/2024/12/21/1_About.me是一个具体业务（即访问指定的一篇博客）
1. Tomcat的连接器负责处理了应用层协议和监听端口的相关内容，并通过设计4层容器（父子关系）来处理特定域名上的特定服务的特定业务请求

##### 各层容器的职能
1. Engine ：顶层容器（只有该容器是只能有一个）
  - 通过Service与连接器交互（连接器的Adapter会通过Service调用Engine的invoke方法）
  - 管理下层的Host容器，根据web请求的域名将请求交给对应的Host容器处理

1. Host ：代表一个虚拟主机，与一个指定域名绑定（本机ip虽然唯一，但是ip却能有多个映射域名，因此Host负责这部分的映射）
  - 管理下层的Context容器，根据web请求的路径来确定请求哪个服务，从而交给对应的Context容器处理

1. Context ：代表一个Web服务
  - 管理下层的Wrapper容器，根据具体的请求路径，把该业务交给对应的Wrapper处理

1. Wrapper ：最底层容器，管理一个Wrapper，负责处理具体业务

##### Pipeline-Valve管道（多层容器处理，转发请求/响应的实现：责任链模式）
1. 每个容器都会维护自己的一个Pipeline链表，元素为Value节点
  - 每个Value都可以对请求/响应进行处理，在把请求/响应交给下一个节点
  - 每层容器的pipeline链尾（Basic节点）都会指向下层容器的表头（First节点）
  ![](https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202507262311018.png)


### Jetty
#### 整体架构（和Tomcat是类似的）
1. 两大组件 ：Connector连接器 和 Handler处理器
1. 全局线程池 ：ThreadPool
1. 管理组件 ：Server（管理上述组件的生命周期）
![](https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202508242222622.png)

#### Connector
> jetty只支持NIO，围绕nio组件（channel连接，Buffer数据在这读写，Selector多路复用监听IO事件），连接器划分出4个小组件  

- Acceptor（Runnable） ：用于使用channel监听并建立连接
  - 服务启动时，会创建指定数量的acceptor去监听(阻塞)web连接
  - 监听到请求后，把channle设置为非阻塞并交由 SelectorManager 处理
- SelectorManager ：管理 ManagedSelector（会把收到的channle分发给他们处理：发放一个Accept任务）
  - ManagedSelector在任务中会把channel注册到NIO的Selector用于监听io事件
- EndPoint ：负责底层数据读取/写入
  - ManagedSelector在Accept任务中时创建；后续通过EndPoint获取一个Runnable任务用于执行数据读取/写入
- Connection ：用于根据具体应用层协议解析数据得到request对象，负责和handler的交互
  - ManagedSelector在Accept任务中时创建；Connection会向EndPoint注册一堆回调方法用于数据读取完毕后解析
![](https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202508242327314.png)

#### Handler（handle方法用于处理请求）
1. Handler为了实现“插件化”的设计思想，使用handler调用链来处理请求（AbstractHandlerContainer：内部有_handler字段，表示内部handler）
1. handler主要分为2种
  - HandlerWrapper ：持有单个内部handler；Server（用于管理服务，需要持有顶层handler引用）和ScopeHandler（用于实现“具有上下文信息”的责任链调用）都是这种
  - HandlerCollection ：持有handler数组，用于支持对不同web服务的handler进行管理


### 参考文章
[深入拆解Tomcat & Jetty](https://learn.lianglianglee.com/%E4%B8%93%E6%A0%8F/%E6%B7%B1%E5%85%A5%E6%8B%86%E8%A7%A3Tomcat%20%20Jetty)  
