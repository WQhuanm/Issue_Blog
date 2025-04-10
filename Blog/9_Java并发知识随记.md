---
title: Java并发知识随记
date: 2025-02-27 06:11:21
categories: 
    - Java
tags: 
    - Java
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202502261916407.png
---

### 一、 线程（Thread）
#### 1. 线程的创建
+ 严格来说，Java 就只有一种方式可以创建线程，那就是通过new Thread().start()创建。
+ 我们定义线程的执行内容则需要重写run方法，使用Lambda实现Runnable函数接口是最为简便的一种方式；也可以继承Thread重写run方法
``` java
public class MyThread extends Thread {
    @Override
    public void run() {}
}

Thread thread = new Thread(() -> {
    System.out.println("Lambda实现了runnable函数接口");
}, "线程1");
```
#### 2. 线程的生命周期和状态
1. 生命周期
    + NEW: 初始状态，线程被创建出来但没有被调用 start() 。
    + RUNNABLE: 运行状态，线程被调用了 start()等待运行的状态。(包括运行态和就绪态)
    + BLOCKED：阻塞状态，需要等待锁释放。
    + WAITING：等待状态，表示该线程需要等待其他线程做出一些特定动作（通知或中断）。
    + TIME_WAITING：超时等待状态，可以在指定的时间后自行返回而不是像 WAITING 那样一直等待。
    + TERMINATED：终止状态，表示该线程已经运行完毕
1. 关于run
    + 调用 start()方法，会启动一个线程并使线程进入了就绪状态，当分配到时间片后就可以开始运行了（自动执行 run()）。
    + 直接执行 run() 方法，只是一个普通方法，不会开启线程
1. Thread.sleep()、Object.wait()、Thread.yield()、Thread.onSpinWait()
    + sleep()没有释放锁，而 wait()释放了锁。
    + wait() 方法被调用后，线程不会自动苏醒，需要别的线程调用同一个对象上的 notify()或者 notifyAll() 方法。或使用 wait(long timeout) 超时后线程会自动苏醒。（为0则不会自动苏醒）
    + yield()表示愿意让出cpu时间片（执行与否取决于OS），可以用于在自旋时减少cpu的消耗，不释放锁
    + onSpinWait()提示jvm当前处于自旋，可以进行优化，不释放锁且占用cpu，不会导致线程状态的切换

1. 线程的中断：Thread.interrupt()
    1. interrupt()本质是设置一个标记位，标识当前线程可以被中断
    1. 流程
        + 当该线程的interrupt()被调用时，设置其中断标记位为true
        + 如果一个线程处于sleep, wait, join 等**可响应中断的**阻塞状态时，若检测到当前线程是可中断的，则会响应抛出InterruptedException异常
            + 抛出异常后catch部分就是对中断逻辑的处理（直接退出，还是处理后继续执行后续代码）
            + 抛出异常后会把中断标记位设为false，以便后续可以继续响应中断
### 二、并发编程
#### 1. 并发编程的三大特性
+ 原子性：Java只有简单的读取、赋值（而且必须是将数字赋值给某个基本数据类型的变量，变量之间的相互赋值不是原子操作）才是原子操作。
+ 可见性：当一个线程对共享变量进行了修改，那么另外的线程都是立即可以看到修改后的最新值。
+ 有序性：代码结果应该与逻辑结果一致（不能因为重排序而改变）

#### 2. JMM（Java 内存模型）
1. JMM规定了并发编程中的一些原则/规范
    1. JMM抽象了线程和主内存之间的关系：划分出了主内存和本地内存（定义线程间的交互规则）
        主内存：存储共享变量，所有线程创建的实例对象都存放在主内存中
        本地内存（不真实存在）：存储共享变量的副本。线程都有一个私有的本地内存，线程只能对本地内存的数据操作
    1. happens-before 原则（强调并发的可见性）
        + 为了对编译器和处理器的约束尽可能少，只要不改变程序的执行结果，编译器和处理器怎么进行重排序优化都行。
        + 对于会改变程序执行结果的重排序，JMM 要求编译器和处理器必须禁止这种重排序。

#### 3. 并发同步的实现
##### 1. volatile 关键字(只能修饰变量，保证变量的可见性和有序性，不保证原子性)
+ 有序性的实现：对修饰变量操作时，会通过插入特定的内存屏障的方式来禁止指令重排序。
+ 可见性的实现：修饰的变量每次修改需要立刻同步到内存，每次读取必须从内存读取

##### 2. synchronized关键字(可重入锁、非公平锁、不可中断锁。修饰类/方法/代码块)
1. 锁的用法
    + 对实例方法加锁，获得**对象锁**，当前对象的**所有实例方法**只有拥有对象锁的线程才能访问
    + 对静态方法加锁，获得**类锁**(synchronized(class))，类的**所有静态方法**只有拥有类锁的线程才能访问
    + 类锁和对象锁不互斥，类锁被锁定时，仍然可以访问对象实例
    + synchronized(String a)需要考虑字符串常量池问题
1. 锁升级(无锁->(偏向锁->)轻量级锁->重量级锁)
    ![](https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202502262030106.png)
    1. 当一个共享资源首次被某个线程访问时，锁就会从无锁状态升级到偏向锁状态，偏向锁会在Markword的偏向线程ID里存储当前线程的操作系统线程ID，此后如果当前线程再次进入临界区域时，不需要进行加锁或解锁操作，只比较这个偏向线程ID即可，优化单线程访问。当有多个线程竞争同一个锁时，则锁状态会从偏向锁升级到轻量级锁，
    1. 如果未开启偏向锁，有线程访问共享资源则直接由无锁升级为轻量级锁。轻量级锁通过自旋锁的方式实现，即当一个线程尝试获取锁时，会在原地循环等待，而不是阻塞线程
    1. 当轻量级锁的自旋次数超过阈值，锁会升级为重量级锁。重量级锁依赖于操作系统的互斥锁（Mutex Lock）实现，会导致线程阻塞和唤醒的开销增加，从而降低性能
1. synchronized 底层原理
    + JVM中每个对象实例和类的class对象 中都内置了一个Monitor（在对象头里，实现同步的基础）
    1. 可见性的保证（内存屏障）
        + 进入同步块时（获取锁）：清空本地工作内存，强制从主内存重新加载所有共享变量的最新值（Load Barrier）。
        + 退出同步块时（释放锁）：将本地工作内存中修改的共享变量刷新到主内存（Store Barrier）。
    1. synchronized修饰代码块时
        + 使用monitorenter指令指向同步代码块的开始位置，monitorexit指令指明同步代码块的结束位置（2个exit，分别执行代码正常执行以及出现异常的情况）
        + 执行 monitorenter 指令时，就会尝试获取monitor的持有权（即通过获取相应的锁（对象锁/类锁）取得持有权）
    1. synchronized修饰方法时
        + 用ACC_SYNCHRONIZED 标识，指明该方法是同步方法
        + 在同步方法调用时隐式获取对象的 Monitor。


##### 3. AQS（AbstractQueuedSynchronizer，抽象队列同步器）：模板抽象类，由于构建各种同步器/锁
1. AQS的思想：定义了**资源获取和释放**的通用流程，而具体的资源获取逻辑则由具体同步器通过重写模板方法来实现。
1. AQS的核心实现：变体CLH锁
    1. CLH锁基于自旋锁进行优化
        1. 思想：CLH锁用一个队列来组织并发竞争的线程（每个结点记录前驱，尾插法）
            + 每个线程会作为一个节点加入到队列中，并通过自旋监控前一个线程节点的状态（释放锁了没），不再是直接竞争共享变量。
            + 线程按顺序排队，确保公平性，从而避免了 “饥饿” 问题
        1. 优点：解决了高并发下，容易造成某个线程的 CAS 操作长时间失败，从而导致 “饥饿”问题
        1. 缺点：使用自旋等待锁，如果锁长时间不释放，浪费CPU
    1. AQS改进的CLH锁
        + 引入了 自旋 + 阻塞 的混合机制：先短暂自旋尝试，如果仍然失败，则线程会进入阻塞状态，等待被唤醒
        + 使用双向队列：节点释放锁时，通过next指针唤醒后续节点
        + 结点设置waitStatus状态：活跃状态为0，阻塞状态为SIGNAL,异常状态为CANCELLED（即取消获取锁，则无法被唤醒，也无法唤醒后继节点）
        + 通过CAS操作来控制 队列初始化 、线程节点入队 两个操作的并发安全
1. AQS的临界资源：state（volatile 修饰）
    + 独占模式下（如可重入锁）：state表示锁被重入次数，0表示资源空闲
    + 共享模式下（如Semaphore：信号量）：state表示剩余临界资源数量，<0表示临界资源获取需要排队等待

1. AQS资源共享方式及获取/释放逻辑
    + 两种资源共享方式：Exclusive（独占）和Share（共享）
    + 自定义同步器只需要实现tryAcquire-tryRelease 或 tryAcquireShared-tryReleaseShared方法（钩子方法：抽象类定义该方法，由子类扩展）
    + AQS具体实现了资源获取/释放时如何操作CLH队列，继承者只需要实现资源具体如何获取/释放（即try方法）

1. AQS 独占模式下资源获取/释放分析（共享模式同理）
    1. 资源获取：入口方法是acquire(int arg)
        1. acquire()会先尝试获取共享资源：tryAcquire()
        1. 如果获取失败，会将线程封装为Node节点加入到 AQS 的等待队列中
        1. 线程在等待队列中尝试获取资源，失败会尝试阻塞该线程
            + 前驱状态阻塞（SIGNAL），阻塞线程
            + 前驱状态异常（CANCELLED），更换其前驱，再次尝试获取资源
        1. 加入队列时，若因超时或中断退出循环，设置结点为cancled，并清理队列（队列每次出现cancled结点，都会从tail开始重新整理队列，清除内部cancled结点，保证每个结点的后驱都是有效后驱）
    1. 资源释放：入口方法是 release(int arg)
        1. 执行tryRelease()尝试释放
        1. 如果锁释放，唤醒后继结点

##### 4. ReentrantLock
1. 基本介绍
    1. ReentrantLock本质是使用AQS实现，内部有3个内部类Sync、NonfairSync、FairSync（后2者继承Sync）
    1. 其内部类的实现方式，使得ReentrantLock具有可重入性，可为非公平锁（默认）、公平锁
        + 非公平锁：后来线程可插队
        + 公平锁：先来先服务，需要增加AQS的队列的阻塞和唤醒的时间开销
    1. 继承自Lock（可中断锁）
        + 有lock()获取锁，获取不到一直等待
        + tryLock()尝试获取锁，返回成功失败，可设置等待时间
        + lockInterruptibly()获取锁，获取不到等待时可被中断

1. Sync的实现
    + tryRelease():将AQS的state-1，如果为0，释放锁，执行后续唤醒后驱流程

1. NonfairSync的实现
    + initialTryLock()：lock时会先执行再执行acquire，当资源空闲直接拿，否则若锁为当前线程占有，重入，否则执行acquire
    + tryAcquire():如果资源空闲，拿取，否则执行后续流程

1. FairSync的实现
    + initialTryLock()：lock时会先执行再执行acquire，当资源空闲且AQS队列为空，获取；否则若锁为当前线程占有，重入，否则执行acquire
    + tryAcquire():当资源空闲且AQS队列为空，获取


#### 4. 乐观锁、悲观锁
+ 悲观锁：共享资源每次只给一个线程使用，其它线程阻塞，用完后再把资源转让给其它线程。
+ 乐观锁：适用竞争较少场景，无需加锁也无需等待，只是在提交修改的时候去验证对应的资源是否被其它线程修改了（版本号机制或 CAS 算法）
    1. 版本号机制：数据维护version信息，线程更新时，在读取数据的同时也会读取 version 值，提交更新时只有当前version与之前读的一致才更新，并把version增加，否则重试更新操作，直到更新成功。
    1. CAS(Compare And Set)算法：CAS 是一个原子操作，就是用一个预期值和要更新的变量当前值进行比较，两值相等才会进行更新，否则重试
    1. CAS的一些问题
        + CAS算法存在ABA问题：读时为A，更新时确认也为A，不能保证中间未被修改为B（解决方法是追加版本号或者时间戳）
        + 循环时间长开销大：CAS 经常会用到自旋操作来进行重试，也就是不成功就一直循环执行直到成功。


#### 5. ThreadLocal（每个线程有专属本地变量）
![](https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202502262327509.png)
1. 原理
    + ThreadLocal有个静态内部类ThreadLocalMap（类似hashmap），以ThreadLocal为Key，Object为value，用Entry存取。一个线程每创建一个ThreadLocal可以存取一个变量副本
    + Thread有个ThreadLocalMap属性(初始为null)，ThreadLocal存入变量副本，是存入到当前Thread的ThreadLocalMap里面
1. 内存泄漏
    + ThreadLocalMap 中的 key 是 ThreadLocal 的弱引用 (WeakReference<ThreadLocal<?>>)，当ThreadLocal实例不再被任何强引用指向，垃圾回收器会在下次GC时回收该实例，导致 ThreadLocalMap 中对应的 key 变为 null。（若使用强引用，只要线程不死，ThreadLocla就会一直存在）
    + ThreadLocalMap 中的 value 是强引用。 即使 key 被回收（变为 null），value 仍然存在于 ThreadLocalMap 中，被强引用，不会被回收。
    + 当ThreadLocal 实例不再被强引用,且线程持续存活（线程池使线程复用等），使ThreadLocalMap长期存在，则会导致 key 为 null 的 entry 无法被垃圾回收，就会造成内存泄漏。
    + 使用完 ThreadLocal 后，调用 remove() 方法显式删除entry是避免内存泄漏的不错方法
    + ThreadLocalMap自清理的方式：
        1. 探测式清理（expungeStaleEntry()）：从当前节点开始遍历数组，key==null的将entry置为null
        2. 启发式清理（cleanSomeSlots()）：从当前节点开始，进行do-while循环检查清理过期key，结束条件是连续log（数组长度）次未发现过期key就跳出循环
        1. 执行set，get，rehash，remove时就会触发上述清理流程

### 三、线程池
#### 1. Executor 框架（包括了线程池的管理，还提供了线程工厂、队列以及拒绝策略等），由三大部分组成
+ 任务(Runnable /Callable，Runnable不会返回结果或抛出检查异常，但Callable可以。)
+ 任务的执行(Executor)
+ 异步计算的结果(Future)：（调用 submit() 方法时会返回一个 FutureTask 对象）

#### 2. 常见线程池
+ FixedThreadPool：固定线程数量，避免频繁创建和销毁线程。使用无界队列LinkedBlockingQueue，可能堆积大量的请求，从而导致 OOM(OutOfMemoryError)
+ SingleThreadExecutor：只有一个线程，保证任务顺序执行。使用无界队列LinkedBlockingQueue，可能堆积大量的请求，从而导致 OOM
+ CachedThreadPool：无核心线程，无最大线程数限制，适用于大量短生命周期任务，线程可以快速回收和重用。使用同步队列SynchronousQueue,可能会创建大量线程，从而导致 OOM。
+ ScheduledThreadPool 核心线程数为 corePoolSize，无最大线程数限制，可执行定时任务和周期性任务。使用无界延迟阻塞队列DelayedWorkQueue，可能堆积大量的请求，从而导致 OOM。

#### 3. ThreadPoolExecutor(线程池实现类（用于自定义线程池）,  是 Executor 框架最核心的类)
1. 线程池处理任务流程
    1. 当前线程数小于核心线程数，新建一个线程执行任务。
    1. 否则若等待队列未满，把任务放入到任务队列里等待执行。
    1. 若任务队列已满，但当前线程数<最大线程数，就新建一个线程来执行任务。
    1. 若当前线程数=最大线程数，执行拒绝策略
1. 线程池常用阻塞队列
    + 无界队列LinkedBlockingQueue：容量为 Integer.MAX_VALUE
    + 同步队列SynchronousQueue：没有容量，不存储元素，目的是保证对于提交的任务被即使使用线程处理
    + 延迟阻塞队列DelayedWorkQueue：内部采用“堆”数据结构，按照延迟的时间长短对任务进行排序。元素满了会自动扩容原来容量的 1/2，即永远不会阻塞，最大扩容可达 Integer.MAX_VALUE
1. 4种拒绝策略
    1. AbortPolicy：默认策略，抛出 RejectedExecutionException来拒绝新任务的处理。
    1. CallerRunsPolicy：调用执行自己的线程运行任务，如果执行程序已关闭，则会丢弃该任务。存在风险，若是主线程提交任务，可能会导致主线程阻塞，影响程序的正常运行。
    1. DiscardPolicy：不处理新任务，直接丢弃掉。
    1. DiscardOldestPolicy：此策略将丢弃最早的未处理的任务请求。
1. 线程池线程数设定公式
    1. 核心线程数
        + CPU 密集型任务(线程数：N+1，N为CPU 核心数)：+1是为了防止线程因缺页中断等原因导致的任务暂停而带来的影响。一旦任务暂停，CPU 就会处于空闲状态，而在这种情况下多出来的一个线程就可以充分利用 CPU 的空闲时间。
        + I/O 密集型任务(2N)：线程在处理 I/O 的时间段内不会占用 CPU 来处理，这时就可以将 CPU 交出给其它线程使用
    1. 最大线程数(一般设置为核心的一倍：保证即使多来一些任务，任务也能占有原本核心线程时一半的cpu时间)
        + CPU 密集型任务：2N
        + I/O 密集型任务：4N
1. 使用ThreadPoolExecutor构建线程池
```java
/**
* 线程池核心参数
    corePoolSize : 核心线程数量，任务队列未达到队列容量时，最大可以同时运行的线程数量。
    maximumPoolSize : 最大线程数，任务队列中存放的任务达到队列容量的时候，当前可以同时运行的线程数量变为最大线程数。
    workQueue: 任务队列， 新任务来的时候会先判断当前运行的线程数量是否达到核心线程数，如果达到的话，新任务就会被存放在队列中。
* 其他参数
    keepAliveTime:非核心线程空闲时可存货时间
    unit : keepAliveTime 参数的时间单位。
    threadFactory :线程工厂，用来创建线程，一般默认，不用设置
    handler :拒绝策略
**/

    //创建线程池
    ThreadPoolExecutor executor = new ThreadPoolExecutor(CORE_POOL_SIZE, MAX_POOL_SIZE, KEEP_ALIVE_TIME, TimeUnit.SECONDS,
            new ArrayBlockingQueue<>(QUEUE_CAPACITY), new ThreadPoolExecutor.CallerRunsPolicy());
    //制定任务
    Runnable worker=()->{
        System.out.println(Thread.currentThread().getName() + " Start. Time = " + new Date());
    };
    //提交任务
    executor.execute(worker);//excute提交任务，无返回结果
    Future<?> result = executor.submit(worker);//submit提交任务并把任务函数返回值封装到future
    try {
        System.out.println(result.get());
    } catch (Exception e) {
        System.out.println(e.getMessage());
    }
    //终止线程池
    executor.shutdown();
    //终止线程池后，等待正在执行任务结束
    while (!executor.isTerminated()) ;
    System.out.println("Finished all threads");
```
1. sumbit()执行任务与excute()执行任务
    + execute()未捕获异常会导致线程终止，线程池创建新线程替代；submit()会把异常封装在Future中，线程继续复用。    
    + execute()用于提交不需要返回值的任务，无法判断任务是否被线程池成功执行；submit()返回一个 Future 对象，通过这个 Future 对象可以判断任务是否执行成功，并获取任务的返回值(Future.get())



<!-- 1. ReentrantLock，AQS -->
