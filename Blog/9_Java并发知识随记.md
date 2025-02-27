---
title: Java并发知识随记
date: 2025-02-27 06:11:21
categories: 
    - Java
tags: 
    - Java
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202502261916407.png
---

1. 线程（Thread）
    1. 线程的创建（严格来说，Java 就只有一种方式可以创建线程，那就是通过new Thread().start()创建。）
        我们定义线程的执行内容则需要重写run方法，使用Lambda实现Runnable函数接口是最为简便的一种方式；也可以继承Thread重写run方法
        ``` java
        public class MyThread extends Thread {
            @Override
            public void run() {}
        }

        Thread thread = new Thread(() -> {
            System.out.println("Lambda实现了runnable函数接口");
        }, "线程1");
        ```
    1. 线程的生命周期和状态
        + NEW: 初始状态，线程被创建出来但没有被调用 start() 。
        + RUNNABLE: 运行状态，线程被调用了 start()等待运行的状态。(包括运行态和就绪态)
        + BLOCKED：阻塞状态，需要等待锁释放。
        + WAITING：等待状态，表示该线程需要等待其他线程做出一些特定动作（通知或中断）。
        + TIME_WAITING：超时等待状态，可以在指定的时间后自行返回而不是像 WAITING 那样一直等待。
        + TERMINATED：终止状态，表示该线程已经运行完毕
    
        调用 start()方法，会启动一个线程并使线程进入了就绪状态，当分配到时间片后就可以开始运行了（自动执行 run()）。
        直接执行 run() 方法，只是一个普通方法，不会开启线程
    1. Thread.sleep()和Object.wait()
        sleep()没有释放锁，而 wait()释放了锁。
        wait() 方法被调用后，线程不会自动苏醒，需要别的线程调用同一个对象上的 notify()或者 notifyAll() 方法。或使用 wait(long timeout) 超时后线程会自动苏醒。（为0则不会自动苏醒）

1. 并发编程的三大特性
    + 原子性：Java只有简单的读取、赋值（而且必须是将数字赋值给某个基本数据类型的变量，变量之间的相互赋值不是原子操作）才是原子操作。
    + 可见性：当一个线程对共享变量进行了修改，那么另外的线程都是立即可以看到修改后的最新值。
    + 有序性：代码结果应该与逻辑结果一致（不能因为重排序而改变）


1. JMM（Java 内存模型）
    JMM规定了并发编程中的一些原则/规范
    1. JMM抽象了线程和主内存之间的关系：划分出了主内存和本地内存
        主内存：存储共享变量，所有线程创建的实例对象都存放在主内存中
        本地内存（不真实存在）：存储共享变量的副本。线程都有一个私有的本地内存，线程只能对本地内存的数据操作
    1. happens-before 原则（强调并发的可见性）
        + 为了对编译器和处理器的约束尽可能少，只要不改变程序的执行结果，编译器和处理器怎么进行重排序优化都行。
        + 对于会改变程序执行结果的重排序，JMM 要求编译器和处理器必须禁止这种重排序。
        
1. volatile 关键字(只能修饰变量，保证变量的可见性和有序性，不保证原子性)
    + 有序性的实现：对修饰变量操作时，会通过插入特定的内存屏障的方式来禁止指令重排序。
    + 可见性的实现：修饰的变量每次修改需要立刻同步到内存，每次读取必须从内存读取

1. synchronized关键字(可重入锁，修饰类/方法/代码块)
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

1. 乐观锁、悲观锁
    + 悲观锁：共享资源每次只给一个线程使用，其它线程阻塞，用完后再把资源转让给其它线程。
    + 乐观锁：使用竞争较少场景，无需加锁也无需等待，只是在提交修改的时候去验证对应的资源是否被其它线程修改了（版本号机制或 CAS 算法）
        1. 版本号机制：数据维护version信息，线程更新时，在读取数据的同时也会读取 version 值，提交更新时只有当前version与之前读的一致才更新，并把version增加，否则重试更新操作，直到更新成功。
        1. CAS(Compare And Swap)算法：CAS 是一个原子操作，就是用一个预期值和要更新的变量当前值进行比较，两值相等才会进行更新，否则重试
        1. CAS的一些问题
            + CAS算法存在ABA问题：读时为A，更新时确认也为A，不能保证中间未被修改为B（解决方法是追加版本号或者时间戳）
            + 循环时间长开销大：CAS 经常会用到自旋操作来进行重试，也就是不成功就一直循环执行直到成功。


1. ThreadLocal（每个线程有专属本地变量）
    ![](https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202502262327509.png)
    1. 原理
        + ThreadLocal有个静态内部类ThreadLocalMap（类似hashmap），以ThreadLocal为Key，Object为value，用Entry存取。一个线程每创建一个ThreadLocal可以存取一个变量副本
        + Thread有个ThreadLocalMap属性(初始为null)，ThreadLocal存入变量副本，是存入到当前Thread的ThreadLocalMap里面
    1. 内存泄漏
        + ThreadLocalMap 中的 key 是 ThreadLocal 的弱引用 (WeakReference<ThreadLocal<?>>)，当ThreadLocal实例不再被任何强引用指向，垃圾回收器会在下次GC时回收该实例，导致 ThreadLocalMap 中对应的 key 变为 null。
        + ThreadLocalMap 中的 value 是强引用。 即使 key 被回收（变为 null），value 仍然存在于 ThreadLocalMap 中，被强引用，不会被回收。
        + 当ThreadLocal 实例不再被强引用,且线程持续存活（线程池使线程复用等），使ThreadLocalMap长期存在，则会导致 key 为 null 的 entry 无法被垃圾回收，就会造成内存泄漏。
        + 使用完 ThreadLocal 后，调用 remove() 方法显式删除entry是避免内存泄漏的不错方法

1. 线程池
    1. Executor 框架（包括了线程池的管理，还提供了线程工厂、队列以及拒绝策略等），由三大部分组成
        + 任务(Runnable /Callable，Runnable不会返回结果或抛出检查异常，但Callable可以。)
        + 任务的执行(Executor)
        + 异步计算的结果(Future)：（调用 submit() 方法时会返回一个 FutureTask 对象）

    1. 常见线程池
        + FixedThreadPool：固定线程数量，避免频繁创建和销毁线程。使用无界队列LinkedBlockingQueue，可能堆积大量的请求，从而导致 OOM(OutOfMemoryError)
        + SingleThreadExecutor：只有一个线程，保证任务顺序执行。使用无界队列LinkedBlockingQueue，可能堆积大量的请求，从而导致 OOM
        + CachedThreadPool：无核心线程，无最大线程数限制，适用于大量短生命周期任务，线程可以快速回收和重用。使用同步队列SynchronousQueue,可能会创建大量线程，从而导致 OOM。
        + ScheduledThreadPool 核心线程数为 corePoolSize，无最大线程数限制，可执行定时任务和周期性任务。使用无界延迟阻塞队列DelayedWorkQueue，可能堆积大量的请求，从而导致 OOM。

    1. ThreadPoolExecutor(线程池实现类（用于自定义线程池）,  是 Executor 框架最核心的类)
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
        1. 线程池大小设定公式
            + CPU 密集型任务(线程数：N+1，N为CPU 核心数)：+1是为了防止线程因缺页中断等原因导致的任务暂停而带来的影响。一旦任务暂停，CPU 就会处于空闲状态，而在这种情况下多出来的一个线程就可以充分利用 CPU 的空闲时间。
            I/O 密集型任务(2N)：线程在处理 I/O 的时间段内不会占用 CPU 来处理，这时就可以将 CPU 交出给其它线程使用
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
