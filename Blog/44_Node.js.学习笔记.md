---
title: Node.js 学习笔记
date: 2025-07-24 09:23:56
mathjax: true
categories: 
    - CS基础
tags: 
    - Node.JS
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202507270022366.png
---


### JavaScript 基本语法
1. 变量声明
    - const: 声明为常量，不可修改
    - let：可修改变量
    - var: 变量可重复声明
        - 函数作用域：在一个函数某处声明，函数全局可访问到
        - 有“变量提升”的特性：会把变量声明提升到作用域顶部，有风险

1. 数据类型
    + 基本类型
        - String ：可使用'',"",\` \` 来定义字符串，其中\` \`可使用${}引用变量
        - Number ：包括整数/浮点数，范围是2^53
            - 大范围可使用BigNumber（数字末尾带n来区分，如1234n）
            - NaN (Not a Number) ：表示一个非法数字结果，且NaN不等于自身(使用isNaN()判断)
        - undefined ：未定义（访问不存在的字段即为undefined）
    + 类型判断
        - typeof ：除了基本的数据类型，还有undefined，function，除此之外其余类型都是object(null 也是object)
        - Object.prototype.toString.call(目标对象) ：可以区分更细致的数据类型（如"[object Array]","[object Null]"）
            - [Object.prototype](https://zhuanlan.zhihu.com/p/52127423) ：原型对象，大多对象都继承他，其toString会返回该对象的类型
            - call(目标对象) ：指定Object.prototype.toString的this值为当前对象，以输出当前对象的类型
    + 运算符
        - ==与===
            - ==在比较时，类型不同会尝试转换再比较
            - ===是严格比较，类型不同直接false
    + 对象(下面记一个对象为cur)
        - 判断属性是否存在
            - cur.hasOwnProperty("xxx") ：判断对象自身是否有该属性
            - "xxx" in cur ：判断对象自身或者其原型链上是否存在该属性
        - 对象的遍历
            - for key in cur：会遍历对象的所有属性key（不是值）
            - for value of cur ：遍历可迭代对象（如Array,Map,Set等）的值
                - 遍历普通对象时，常写成 for key of Object.keys(cur) ：Object.keys(cur)会返回cur所有**自身属性**的key作为一个数组
    + JSON(JavaScript Object Notation)
        - js可以通过require(json文件)把该文件解析为一个object对象
        - js内置了JSON.stringify()和JSON.parse() 分别用于json化对象/解析json对象

1. 函数
    + 函数属于对象，函数名就是变量 ，如function a(){}等价于a =function(){} 或 a=()=>{}）
    + 方法（在对象内部定义的函数称为方法，每个方法都有this关键字，指向调用当前方法的对象）
        -  call()：每个方法都有call(thisArg,arg1,arg2,...)，用于重新指定执行方法的this上下文对象
    + Array的常用方法/高阶函数（即参数是方法）
        - map(callback(currentValue, index, array)) ：将当前数组通过函数处理后映射为另一个数组
            - 函数3个参数分别是当前元素值，元素索引，原数组本身（后2者传参时可选）
            - filter(),sort()同理
            - 不过sort不会创建新数组，是基于原本数组修改，且sort默认基于字符串排序
        - reduce(callback(accumulator, currentValue, index, array), initialValue) ：将当前数组的元素通过函数归约为一个最终结果
            - 处理函数前2个参数是当前累计处理的结果（该结果是上次处理函数的返回值），以及当前元素，后2个参数可省略
            - initialValue表示处理函数处理的初始值，可选，未设定时数组第一个元素作为初始值

1. 异步函数
    + Promise对象 ：用于封装异步函数
        - Promise构造函数 ：new Promise((resolve,reject)=>{}) ，以一个执行函数为参数（该函数接受2个参数：resolve 和 reject）
            - 执行函数成功执行时，应调用resolve(result) 将result作为结果返回
            - 执行函数执行非法时，应调用reject(reason) 返回错误原因
        - Promise对象的状态 ：Pending (进行中)，Fulfilled (已成功)，Rejected (已失败)
        - Promise 链式调用 ：对Promise执行结果的处理
            - then 方法可接受2个参数：onFulfilled,onRejected（对应resolve，reject）
                - then(onFulfilled, onRejected)等价于then(onFulfilled).catch(onrejected)
                - 处理方法可以写成then(res){} 或者 then((res)=>{})
        - Promise状态返回值规则（返回结果本身也是一个Promise）
            1. 有返回值A，则实例方法返回 状态为 fulfilled、值为 A 的 Promise；
            1. 没有返回值，则实例方法返回 状态为 fulfilled、值为 undefined 的 Promise；
            1. 抛出一个错误，则实例方法返回 状态为 rejected、值为抛出的错误 的 Promise；
            1. 返回一个 Promise(P)，把该Promise(p)返回
    + async/await ：使用async修饰的异步函数会自动封装为Promise，await只能在async函数中使用



### Node.js
#### npm (Node Package Manager)
+ package.json
    - 管理npm依赖
        - dependencies ：项目运行必须依赖
        - devDependencies ：开发测试时需要用的依赖（npm install --production 时会跳过这些依赖）
    - 定义项目自动化脚本（通过npm xxx 可执行相关命令，比如npm test执行全部测试
        - "start" ：定义项目启动的命令（即 node 启动文件）
        - "test" ：指定测试用的依赖包，如mocha，jest
        ``` json
        "scripts": {
            "start": "node ./bin/www",
            "test": "mocha"
        }
        ```
    - 设置项目模块类型：type:"module" 则默认为ESM模块，不设置默认为CommonJS模块

#### 模块化
> 模块是nodejs一开始引入的概念，nodejs的默认模块是commonJS模块，后来js官方推出了ECMAScript Modules(ESM)模块

##### CommonJS（文件扩展名.cjs）
1. 模块加载 ：同步加载（运行时加载）
    - 当代码执行到require时才加载相应模块，且同步加载结束才会继续往下执行（因此不允许在顶层使用await阻塞等待异步函数）
    - 运行时加载的好处是可以动态导入模块
1. 模块导出 ：module.exports 或 exports
    - module本质是一个对象，其属性exports初始是{}，用来存储导出内容
    - exports是初始时指向module.exports的一个引用（可以通过给exports添加属性来导出）
        - 一旦exports被赋值改变指向，或者module.exports被赋值而导致exports不再指向它：exports都将失效，因此不推荐使用
1. 模块导入 ：require 
    - require在导入时是去获取module.exports当前指向的值        

##### ESM （文件扩展名.mjs，该模式默认使用'use strict'严格模式）
1. 模块加载 ：静态分析并预加载
    - 要求模块导入模块是确定的，并把import提升到顶部，在加载模块时就执行导入（加载过程异步，因此运行顶层await）
    - 异步加载，支持顶层await，可以通过await import()这个异步函数来动态导入模块
1. 模块导出 ：export
1. 模块导入 ：import
    - 要求导入名称与导出时相同，使用{}包裹
    - 也可使用import * as xxx 将所有命名导出为一个对象

### Web模块
#### express(对web请求处理和响应)
> 可以使用命令：npx express-generator 生成基本的express程序骨架

1. 核心实例
    - express(): Web应用程序实例，Express 应用的总入口
    - express.Router(): Express的路由实例，用于实现分组路由/中间件，必须挂载到express实例或者其他router实例上。

1. 基本路由格式：router.METHOD(PATH, HANDLER)
    + router是一个路由实例或express实例，METHOD为http请求方法(get,post,....)
    + path为指定请求路径（可使用正则匹配）
    + handler为处理方法(err,req,res,next)=>{}（err和next可省略）

1. 中间件：通过router.use(path,handler)来挂载中间件函数(类似router.Method())
    + 错误处理中间件：函数必须4个参数时定义为错误处理函数：(err, req, res, next)，会把前面处理函数抛出异常在此捕获处理
    + 常用内置/第三方中间件
        - express.json() ：解析JSON格式的请求体数据
        - express.urlencoded() ：解析客户端发送到服务器的 URL-encoded(application/x-www-form-urlencoded) 格式的请求体数据（即URL查询字符串等格式）
        - express.static(req_path,file_path) ：使指定路径的资源文件可以被http访问
            - 常用方法是：express.static(path.join(__dirname, 'resources')),将resource文件夹内静态资源设为可访问
        - cookieParser() ：解析cookie，第三方模块cookie-parser提供

1. request对象
    + 请求参数
        - 路由参数 (Route Parameters) ：URL中特定位置的值，使用:标识(如 /users/:userId)，保存在req.params对象中，key为路由参数名称
        - 查询字符串参数 (Query String Parameters) ： URL中查询字符串(?key1=value1&key2=value2)的参数，保存在req.query对象中
        - 请求体(Query Body) ：

1. response对象
    + 响应方法 ：调用响应方法后即标识请求处理结束。不响应又不调用next(),会导致该请求被挂起，导致客户端最终请求超时
        - res.send(data) ：发送数据，会根据data类型设置Content-Type（如json，html，纯文本等）
        - res.redirect(path) ：请求重定向到指定路径,路径格式如下
            - 完整url
            - /开头：以当前域名的根目录开始
            - 不以/开头：当前请求url的相对路径

#### axios（发送web请求）
- get ：axios.get(url,params:{}).then(response=>{}) 
    - params 会拼凑成查询字符串
- post ：axios.post(url,body).then(response => {})

### 常用模块
#### child_process
1. child_process.exec(command,(err,stdout,stderr)=>{}) ：异步执行命令
1. child_process.execSync(command) ：同步执行命令，成功返回stdout

### 参考
[用了几年的Promise，竟然还搞不清楚返回值是什么～](https://juejin.cn/post/7196689993082978363#heading-3)  
[JavaScript教程-廖雪峰](https://liaoxuefeng.com/books/javascript/introduction/index.html) 
[Express 中文文档](https://www.expressrc.cn/)  

