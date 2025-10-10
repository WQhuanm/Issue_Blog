---
title: CPP学习笔记
date: 2025-09-26 08:03:33
mathjax: true
categories: 
    - CS基础
tags: 
    - C++
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202509261428721.png
---


### 基础语法
#### 数据类型相关
- 数组
    - 初始化arr[num]时
        - 指定num，则内存空间根据num计算
        - 如果使用了初始化列表`arr[num]={val1,val2}` 
            - 不指定num时，内存空间就是初始化元素数量（不会给char[]自动追加'\0'）
            - 指定num时，用于初始化前几个元素
        - 如果是char数组，使用字符串初始化时（如`arr[]="hello"`）,会给数组尾部追加'\0'
    - 数组退化 ：当传递数组参数，或者指针直接指向数组时，数组退化成指向首元素的指针
        - 使用引用参数可避免数组退化（配合模板使用还可自动推导数组长度）  
        ```cpp
        template <size_t N> //N 是一个编译期常量，会推导为数组大小
        void call_by_reference(int (&a)[N]) {//传入数组是int[]，操作引用a和操作原本数组一致
        }
        ```
    - char数组：要求以'\0'结尾
        - 调用读取方法时(cout,strlen等)，会一直往后读取，直到读取到'\0'才结束
        - 如果声明的char数组没有留有空间给'\0'，则上述方法执行可能出现异常（会执行到'\0'为止）

- 函数
    - 函数参数可不带变量名，如果该参数无需使用，只声明参数类型即可,如`void f(int* ){}`

- sizeof ：C++ 编译期间计算的操作符，用于计算数据类型或对象所占用的字节数
    - 计算一个空结构/void方法时默认为1
    - 指针的大小永远是固定的，取决于处理器位数，32位就是 4 字节，64位就是 8 字节
    - 结构体会进行内存对齐 ：以结构体中最大**基本变量**的字节来对齐（包括嵌套结构体内部的变量）
    ```cpp
    struct A{//该结构体内存占12B
        char c1;
        short b;//c1和b合计3B，再填充1B字节
        int a;//4B最大，以他来对齐
        char c2;//占1B，需要再填充3B字节
    };
    ```

- 类型转换
    - 类型转换的本质是值拷贝
        - 如果是指针/引用的转换，则是把指针/引用指向内存中属于新类型的地址拷贝给新指针/引用
        - 如果是对象类型转换（**对象切片**），则是把原本对象中属于新类型的那部分内存拿去给新类型执行拷贝构造函数（即vptr等都会改变）
    - 四种类型转换
        - `static_cast<T>(a)` ：把对象a转为**与a类型相关**的类型T
            - 可以安全的将子类转为父类（会把指针指向父类在子类所属的内存区域）
            - 在编译时进行类型转换，不会做运行时类型检查
        - `dynamic_cast<T>(a)` ：**利用虚指针的机制**（所以被转换类型(即a)必须是**多态类**），可以在运行时实现父子类的安全转换
            - dynamic_cast只能转换指针或引用
                - 它的作用是确保指针/引用在运行时指向的内存一直都记录该内存的实际类型（虚函数表），使得类型操作时一直都是在同一片内存进行操作
                - 而对象切片则会创建一个新对象，与原始对象脱钩
            - 当执行向上类型转换时，实现同static_cast，编译时便类型转换
            - 基类转派生类实现原理
                - 虚函数表(vtable)还存储了**运行时类型信息（RTTI, Runtime Type Information）**，包含了该表所属类的信息和类层次结构
                - 如果是向下转换，则会读取RTTI确定当前指针指向的内存实际类型是否允许转换为目标类型
                    - 编译时期是无法判断一个基类指针指向哪个派生类的
                    - 如果目标类型就是实际类型或者实际类型的基类，则允许转换
                    - 否则如果是指针转换则返回`nullptr`；引用转换则抛出异常`std::bac_cast`
        - `const_cast<T>(a)` ：不支持不同类型的转换，只是用于移除指针/引用的const修饰
            - 不支持对对象转换，因为const本质修饰的是地址（对象转换则会进行拷贝构造了）
        - `reinterpret_cast<T>(a)` ：以目标类型直接解读当前类型的内存。（因此，即使是派生类转换为基类都有可能出错）

#### 指针和引用
- 指针 (`T* p = &x`)
    - 指针p指向对象地址；(*p) 是解引用操作，用于得到对象本身
    - 指针与数组
        - 如果使用 `T * p = arr`,会把arr退化为其首元素的地址（即等价于 `T * p = &arr[0]`），指针类型为元素的指针类型 `T*`
        - 如果使用&引用数组本身 ：`T (\*p)[num] = &arr`，则指针指向数组本身的地址，指针类型为数组本身的指针类型`T(*)[]`
    - 指针数组和数组指针
        - 指针数组 ：存放指针的数组（如 `char * p[num]` ,一个长度为num的数组，元素是`char*`）
        - 数组指针 ：指向的元素是数组的指针（如 `char (*p)[num]`,指针p指向数组的第一个元素：`char[]`，指针类型是`char(*)[num]`）
    - 函数指针与函数声明
        - 函数声明 ：`int* p(int);` 变量名与()结合即为函数，表示名为p，参数为int，返回类型是int*
            - 如果返回类型是数组指针，[]应位于()之后，如`int* (*p(int))[3]`,表示一个函数名为p，参数int，返回类型是`int*(*)[3]`,即指向一个指针数组的指针
        - 函数指针 ：`int (*p)(int)` 指针与()结合即为指向函数的指针，p是指针，指向一个参数为int，返回类型为int的函数
    - 指针常量和常量指针
        - `const T* p` 或 `T const * p`(指针常量) ：指针指向的对象是常量，但指针本身可以修改
        - `T* const p` (常量指针) ：指针本身是常量，不能修改指向，但它指向的对象可以修改
    - 泛型指针`void*` ：`void*`指针可以和其他指针互相转换，但是不能解引用`void*`指针来获取数据（因为不知道数据的实际类型，不知道需要取多少字节）
    - 指针只能访问其类型拥有的成员，即使基类指针指向了派生类的对象，也无法访问派生类独有的成员

- 引用(`T& p = x`)
    - 引用用于作为对象的别名，对引用的任何操作等价于对原本对象的操作
    - 实现类似于常量指针，指向对象所在内存地址；引用不能为空，也不能改变引用对象
    - 使用引用传递参数或者引用方法的返回值可以避免对值的拷贝操作,如 `string& getname(int &id){}`
        - 返回值是引用，则需要使用引用类型来接收
        - 要避免返回值引用是方法的局部变量，会导致悬空引用（返回时引用的局部变量已经被销毁），一般都是返回时引用实例字段

- 左值引用、右值引用、万能引用
    - 左值与右值
        - 左值 ：出现在赋值号左侧，可以被取地址的具名变量。如：`int a = 10;`， `a` 就是左值
        - 右值 ：出现在赋值号右侧，不可被取地址的临时值（临时对象/字面量/函数返回值等）。如：`int a = 10;`， `10` 就是右值
        - std::move() ：可以强行把一个左值**强制转换**为右值引用，用于使用移动语义(底层实现上类似于`static_cast<T&&>(T)`)
            - move用于对象，用于指针是无效的（指针没有移动函数）
            - `std::string s2 = std::move(s1);` ：会把s1转为右值，最终s2的赋值采用移动构造函数
            - `std::string s2 = s1;` ：使用拷贝构造函数赋值s2
    - 左值引用 ：对存在的左值变量进行引用。即常见的`int& b=a;`,b为左值引用，和a指向同一片内存
    - 右值引用 ：对临时变量（右值）进行引用，用于后续实现移动语义。如`int&& a=get();`，a为右值引用，指向原本会立刻被销毁的内存
        - 右值引用是用于接收右值，但是右值引用这个变量本身是左值，离开作用域时才会消失
    - 万能引用 ：即模板`T&&`,接收左值时自动推导为左值引用，接收右值时自动推导为右值引用
        - 完美转发(`std::forward<T>()`) ：将参数的**实际类型**转发给另一个函数（避免右值被具名变量持有时，转发到新函数变成左值等情况）

#### 关键字
- const
    - 修饰成员方法 ：表示执行该函数不会修改对象的成员变量
        - const方法/const对象 只能调用const成员方法
    ```cpp
    class A {
        public:
            int get_val() const {//const方法修改成员变量，则编译会报错
                return value;
            }
        private:
            int value;
        };
    ```

- #define（宏定义） ：用于定义宏变量/函数，编译时会把宏定义进行文本替换，不涉及类型检查

- typedef ：用于给现有类型定义别名，编译时会进行类型检查

- inline ：修饰函数，建议编译器对修饰函数的调用改为把函数体嵌入到调用代码中，消除了函数调用开销

#### 链接与分离式编译 ：使得多个源文件可共享变量/方法
- 函数和变量的 **声明（declaration）与 定义（definition）**
    - 声明 ：告诉编译器该函数/变量/类等的存在，后续会进行定义实现。编译器会为声明留下链接符号，后续执行链接时，会把声明的链接指向定义所在的内存
        - 变量的声明使用extern进行修饰，如`extern int val;`
    - 定义 ：告诉编译器该函数逻辑/变量的值，编译器会为其分配内存空间
- 链接属性 ：如何在编译、链接和执行阶段如何处理符号(定义在全局，变量、函数、类等)的可见性和重复定义
    - 外部链接（External Linkage）：默认的全局变量/函数/类都具有外部链接，外部文件只要进行声明就可以进行访问
    - 内部链接（Internal Linkage）：被static修饰，则为内部链接，被局限作用域为当前文件
    - 外部 C 链接（External C Linkage）：声明链接c语言文件（因为c/cpp的链接实现不相同）
- 分离式编译（Separate Compilation）
    - 代码由多个cpp源文件实现，对多个源文件分别编译后，链接器根据符号的链接将他们组合为一个可执行文件
        - 遵循**一次定义规则（ODR）** ：允许多次声明，要求一次定义，保证链接时定义唯一
    - 具体实现 ：在头文件进行声明，在指定的唯一源文件进行定义
        - 预处理时，头文件代码会被读取并写入每个引用的源文件，形成多次声明
        - 其中的某个文件引入声明同时进行了定义，使得其他文件可进行链接（也避免了多重定义导致链接出错的情况）
        - 实现类似如下代码
        ```cpp
        //c.c
        #include <stdio.h>
        void print_c(){
            printf("hello_c\n");
        }

        //a.h
        #include<string>
        extern int num;
        void a_print(int num);
        extern "C"{//引入c代码的定义
            void print_c();
        }

        /**
        * 对类进行完整声明（实际定义了类)，不过类允许被重复定义（只要定义完全相同，类被视为弱符号）
        * 但是类内部的方法/静态变量不同，他们还是方法/变量（视为强符号），只应该在内存出现一次，因此头文件只进行了声明
        * 对于非静态变量，每次创建对象实例都会给这些变量分配内存，因此允许多个文件重复定义
        */
        class A{
            public:
                void A_print();
                static int val; 
                std::string name="belong to instance";//每个对象
        };

        //a.cpp
        #include "a.h"
        int num=555;
        void a_print(int num){
            printf("a_print : %d\n",num);
        }

        //虽然允许一个类被多个源文件重复定义，但是禁止同一个文件对一个类多次定义，所以只能对类的方法/变量逐个定义
        void A::A_print(){
            printf("%s : %d\n",name.c_str(),val);
        }
        int A::val=666;//静态变量在外部初始化，保证一次定义

        //b.cpp
        #include "a.h"
        int main(){
            a_print(num);
            A a;
            a.A_print();
            print_c();
        }

        /**
        * gcc -c c.c -o c.o //把c源文件-c只编译不链接，生成目标文件
        * g++ a.cpp b.cpp c.o -o final.exe //编译a.cpp和b.cpp，并与* c.o链接后生成最终的可执行文件
        * 输出如下：
        * a_print : 555
        * belong to instance : 666
        * hello_c
        */
        ```
    - 头文件中可进行定义的情况
        - 使用inline修饰的函数可以进行方法定义，链接器会进行特殊处理，确保最终只有一个版本被保留以避免多重定义
        - 头文件定义的模板（要求完整定义），链接时会把重复生成的代码进行特殊处理，确保最终保留一个版本

### 面向对象
#### 类的结构
- 访问权限 ：class类的成员默认private权限，而struct类则是public
- 成员变量
    - 静态成员变量 ：类对象共享，因此该变量只能在类内部进行声明，定义必须在类外部，保证**一次定义规则**
    - 非静态成员变量 ：类对象各自独有，因而可在类内部定义 ：本质是每个对象对自己的成员变量进行一次定义
    - 成员函数 ：类对象共享，存放于.text代码段，调用方法时会通过所属类访问相应代码段
- 特殊成员函数 ：管理对象的生命周期和资源
    - 构造函数 ：构造函数允许隐式调用来转换。如class A有个只含int参数的构造函数时可以执行：`A a=10 `,会隐式改为 `A a= A(10)`
        - explicit修饰 ：禁止隐式转换
        - 构造函数虽然没有返回值，但是可以抛出异常
    - 析构函数 ：在对象生命周期结束清理其占用的资源
        - 析构函数不推荐抛出异常（函数也是被隐式声明为`noexcept`），而且析构被调用，有可能因为出现异常所以有对象被析构，析构函数再抛出则会存在双重异常，则异常传播变得复杂
    - 拷贝构造函数 ：将现有对象用于**创建**新对象。如 `MyClass b = a;` 或 `MyClass b(a);`，默认为浅拷贝
    - 拷贝赋值运算符 ：将现有对象赋值给**现有**对象。如`MyClass b; b=a;`（b前面进行过空初始化了，再使用a给他拷贝赋值）
    - 移动构造函数 ：参数接收右值引用，让**新对象**浅拷贝右值引用，并删除右值引用对其资源的指向
        - 使用noexcept修饰，表示保证不会在移动函数抛出异常（使用该修饰时，vector等容器才会优先使用移动函数）
    - 移动赋值运算符 ：将临时资源移动给**现有**对象，如`MyClass b;b=std::move(a);`
    ```cpp
    class A{
    public:
        int* _val;
        explicit A(int* val) :_val(val){}//通过初始化列表初始化成员，而{}补充其他逻辑
        ~ A(){} // ~表示析构
        A(const A&x):_val(x._val){}//拷贝构造函数，该函数不具返回值
        A& operator=(const A& x){return *this;};//拷贝赋值，返回自身引用以避免返回值拷贝
        A(A&& x) noexcept :_val(x._val){x._val=nullptr;}//移动构造函数
        A& operator=(A&& x){}//移动赋值
    };
    ```

#### 类的继承
- 父类成员访问权限 ：类继承基类时可指定父类成员的访问权限，如`struct B: public A{};`
    - public ：父类成员的访问权限不变
    - private ：父类原本的public/protected在子类都变成了private
    - class类继承父类时默认private继承，struct则是public

- 虚继承(Virtual Inheritance) ：解决多重继承中的**菱形继承问题**
    - 菱形继承问题 ：CPP是支持多继承的。但假设共享基类A有2个派生类B,C，而派生子类D又同时继承B,C，则出现菱形继承问题（A的成员在D中被继承2次）
        - 存在内存浪费
        - 存在二义性 ：操作D的A成员时，不知道操作的是属于B的还是C的
    - 对于这种会被共享的基类(即类A)，他的**直接派生类**（即B，C）应该对他使用虚继承（继承时使用virtual修饰），即表示愿意共享他们虚继承的基类。这会确保基类成员在往后的派生类中（即类D）只存在一份数据
    - 虚继承底层实现原理 ：**虚基类表**（virtual base class table）和**虚基类表指针**（virtual base class pointer）
        - 共享基类在派生子类中，一般会存放于子类内存末尾
        - 使用了虚继承的类，它的对象会内存会有一个虚基类指针(vbcptr)指向虚基类表
            - 虚基类表存放在其他内存空间，本质是一个一维数组
            - 每个类都需要为它的所有虚基类指针**各自**维护一个虚基类表（比如D需要分别为B,C维护），该类的对象共享这个类的所有虚基类表
            - 当前类(D)维护的每个虚基类表记录了 ：共享基类对象（A）在D中的内存相对于虚继承类对象（B，C）在D中的起始地址的偏移量

- 方法隐藏 ：派生类的函数会屏蔽所有与其同名的基类函数

- 虚函数与方法重写
    - 一个类只有包含或继承了虚函数，该类才被视为**多态类**
    - 使用virtual修饰类的非静态成员函数，则该函数可以被派生类重写(override)
        - 纯虚函数 ：只声明不实现，拥有纯虚函数的类为抽象类，无法被实例化
        ```cpp
        class A{
        public:
            virtual void prt(){std::cout<<"a"<<std::endl;}
            virtual void fun()=0;//=0 声明为纯虚函数
        };

        class B : public A{
        public:
            void prt() override{std::cout<<"b"<<std::endl;}
            void fun()override{std::cout<<"fun"<<std::endl;}
        };
        ```
    - 虚函数的实现原理
        - 有虚函数的类会在只读区(.rodata)维护一个该类专用的虚函数表（一维函数指针数组） ：表记录了该类的虚函数们在.text段的地址
        - 有虚函数的类生成的对象会增加一个虚函数表指针(vptr)作为成员变量
        - 基类指针可以指向派生类对象（实际是指向基类在派生类对象中基类对象所属的内存）。
            - 指针调用普通方法时，都是根据指针的实际类型（基类）取获取该类的方法
            - 而调用一个虚函数时，编译器会通过对象的虚函数表指针获取**派生类的虚函数表**，进而获取到派生类实现的方法地址，而不是基类的方法地址
    - 特殊的成员函数与虚函数
        - 构造函数不能是虚函数 ：一个是不同类命名不同，函数不用重写；另一个是构造函数执行时，对象正在初始化，此时vptr不一定被初始化
        - 析构函数在继承中必须是虚函数
            - 如果使用一个基类指针指向派生类对象，delete指针时，如果析构函数不是虚函数，则会出现子类析构未执行,而执行基类析构函数的情况
            - 默认析构函数是无virtual修饰的，以避免虚函数相关的开销。但是如果有派生类，要求定义为虚函数
        - 成员模板函数不能是虚函数
            - 虽然模板函数会在编译时进行实例化，但是一个模板在多个文件的实例化却要等到链接时才能完成组装
            - 而虚函数表在编译阶段就要设置完成，但编译时虚函数表无法确定模板函数最终会有多少实例

#### 对象与内存
- 对象的内存分布
    1. 继承的所有父类们的对象内存
    1. 虚表指针 ：虚函数表指针（如果有虚函数）|| 虚基类表指针（如果该类有直接虚继承父类）
        - 一般2个指针是合并的，即指针指向的内存，既可存虚函数表的数据，也可以存虚基类表的数据
        - 如果类自身定义了虚函数，但是类的父类们已经有虚表指针了，则会复用他们的指针，不再创建新指针
    1. 类自身的非静态成员变量
    1. 共享基类们的对象内存
    - 比如类D继承了B,C，且B,C均虚继承类A，则D的内存布局是
        - [ B的内存布局[虚函数表指针 | 虚基类表指针 | B自身成员变量] | C 的内存布局 | D自身成员变量 | 共享基类A的内存布局 ] 
    - **指针调整** ：当使用基类指针指向派生类对象时，会把指针从指向的对象首地址移动到基类在派生类对象内存中的地址

- 对象的初始化和析构顺序
    - 编译器处理构造函数时，会隐式进行修改
        1. 先调用父类的构造函数进行初始化（cpp可以继承多个类，按照继承时的声明顺序初始化父类（虚继承优先初始化））
        1. 按照成员变量在类中的声明顺序进行初始化（与初始化列表的顺序无关）
        1. 执行类自身的构造函数
    - 析构函数调用顺序则是和初始化完全相反

- 深拷贝与浅拷贝
    - 浅拷贝 ：只复制数据的值。即当复制指针时，只会单纯复制指针指向的地址，不会拷贝指针指向内存所代表的内容，导致拷贝对象和被拷贝对象指针指向同一片内存 
    - 深拷贝 ：会递归复制指针指向的内容

#### 模板（泛型,用于修饰类或方法）
- 模板参数 ：`template<class T ,size_t N,int... args>void f(T a){}` （调用为 `f<int,1e5,1,2,3>(666);`）
    - 可以使用class/typename 声明该参数类型可任意，也可指定具体的参数类型
    - 亦可使用...表示为可变参数
- 模板的特化（即**相对**泛型模板更具体）
    - 我们定义的泛型模板不一定对所有类型都是正确的，因此对于一些特点类型需要在泛型模板的基础上进行特化（更具体的限定参数类型）
        - 部分特化 ：仍然会使用到泛型，可单独存在
            - 多个部分特化模板之间可匹配的参数类型 要么是完全包含的关系，要么不相交
            - 如果存在相交且不包含，函数调用（或者声明完全特化函数时）则不明确使用哪个部分特化模板，存在二义性，会报错
        - 完全特化 ：完全指定了所有参数的具体类型（和非模板函数的区别就是多了个`template<>`），对**前面出现的**模板中**最匹配**的函数重载进行补充指定
        ```cpp
        template<class A, class B>void add(A a, B b){cout<<1<<endl;}
        template<class A, class B>void add(A*a, B b){cout<<2<<endl;}//该泛型是上面泛型的特化
        template<class A, class B>void add(int* a, B b){cout<<3<<endl;}//比上面的特化更特化
        // template<class A>void add(A a,string b){cout<<4<<endl;}//如果使用，则编译错误，与3相交不包含，完全特化不知道补充谁
        template<>void add(int *a,string b){cout<<100<<endl;}//完全特化，对前面出现的模板中最匹配的进行补充，即2
        template<class A>void add(A a,string b){cout<<4.5<<endl;}//这个可以通过编译，因为在完全特化后面，未被识别
        ```
    - 多个模版函数重载时的优先匹配规则
        1. 非模板函数（如果普通函数完全匹配，最优先）
        1. 部分特化模板
        1. 泛型模板
- 模板的实例化
    - 模板本质是一个蓝图（代码生成器）。在编译阶段，编译器读取到使用特定类型的模板时会生成代码并存放到代码区
        - 函数模板会生成具体的函数
        - 类模板会先生成具体类（编译器读取到模板类的成员函数的调用时才会对成员函数实例化）
    - 模板是编译时的工具，编译完成后就不存在了
- 可变参数模板 ：`template<class... Args>void fun(Args... args)`，用于接收0或多个参数
    - `Args`是类型参数包，是函数参数类型的集合（比如声明函数`fun(int,string,double)`,则`Args`等价于`(int,string,double)`）
    - `args`是函数参数包，是函数各个参数类型的值（比如调用`fun(123,"123",1.23)`，则`args`等价于`(123,"123",1.23)`）
    - 参数包的展开（参数包不能直接使用，必须被展开：`args...`会展开为`arg1,arg2,...argN`）
        - 递归展开
        ```cpp
        void FormatPrint(){std::cout << std::endl;}//递归终止函数

        template <class T, class ...Args>
        void FormatPrint(T cur, Args... args)
        {
        std::cout << "[" << cur << "]";
        FormatPrint(args...);//...表示将参数包展开为参数列表，否则参数包会被视为一个整体
        }
        ```
        - 逗号表达式展开
        ```cpp
        template <class T>
        void PrintArg(T t){cout << t << " ";}//处理每个参数的函数
        template <class ...Args>
        void ShowList(Args... args)
        {
            ((PrintArg(args)),...);//逗号表示会把args每个参数都拿去调用左侧函数
        }
        ```

### 内存管理
#### RAII(resource Acquisition Is Initialization,资源获取即初始化)
- 思想 ：将资源的生命周期与某个对象的生命周期绑定
- 利用栈自动析构局部变量的机制来释放资源，使用栈上创建的对象来管理资源
- 封装一个RAII类来管理资源，在构造函数初始化资源，在析构函数释放资源

#### 智能指针
- 智能指针基于RAII实现进行实现，用于代替裸指针来管理指向的**堆内存**(智能指针内部管理该裸指针)  
    - 我们不应该使用智能指针管理**栈对象**的裸指针，会导致对象被双重释放（智能指针离开作用域时释放一次，对象离开作用域又栈被释放）
    - 智能指针的创建推荐使用`std::make_shared<>()`/`std::make_unique<>()`创建，他们会接收对象构造参数来new对象并管理
        - 如果使用`std::shared_ptr<>()`/`std::unique_ptr<>()`，他们接收裸指针来管理，如果外部持有裸指针，那么该裸指针创建的多个智能指针的所有权是独立的
- 智能指针主要分为2种 ：独占指针(`std::unique_ptr`)和共享指针(`std::shared_ptr`)
    - `std::unique_ptr`
        - 强调独占所有权，保证其管理的内存不能被其他智能指针获取（删除了拷贝函数）
        - 调用release会释放其对管理的裸指针的所有权并返回该裸指针。后续需要手动管理该裸指针
    - `std::shared_ptr`
        - 允许共享所有权，维护一个**控制块**来管理信息,控制块包含信息如下
            - 记录强/弱引用的计数指针，相同所有权的计数指针指向同一个内存来维护计数
                - 当强引用归零时才会释放**原始资源**
                - 当弱引用归零时才会释放**控制块资源**
            - 指向原始资源的指针
        - 存在循环引用的问题，可以引入`std::weak_ptr`来打破（不增加引用计数）
            - weak_ptr不能直接访问资源，需要使用`lock()`来获取一个临时的shared_ptr来访问资源，如果资源被释放，则获取到一个空的shared_ptr(布尔值为false)
            - weak_ptr可通过`expired()`方法来判断资源被释放
        - `std::enable_shared_from_this` ：允许我们在对象内部传递指向该对象的this指针的智能指针
            - 如果我们在对象方法内部直接对this指针封装为智能指针并传递，会导致离开方法后，智能指针离开作用域并释放了this对象
            - 而如果类public继承了`std::enable_shared_from_this`，在外部创建了智能指针的情况下，可以调用`shared_from_this()`在对象内部传递智能指针
            - `std::enable_shared_from_this`的思想
                - **弱引用回传** ：内部维护一个weak_ptr，当我们在外部给对象创建shared_ptr时，构造函数检测到有继承`std::enable_shared_from_this`则，向对象的weak_ptr共享所有权
                - 对象内部调用`shared_from_this()`时，本质是执行`weak_ptr::lock()`
        ```cpp
        //shared_ptr简单实现
        template<class T>
        class shared_ptr{
            T* ptr;
            int* count;

            public:
                explicit shared_ptr(T* cur = nullptr):ptr(cur),count(ptr?new int(1):nullptr){}
                ~shared_ptr(){release(); }
                shared_ptr(const shared_ptr& cur):ptr(cur.ptr),count(cur.count){
                    if(count)++(*count);
                }
                shared_ptr& operator=(const shared_ptr&cur){
                    if(this!=&cur){//因为是赋值，因此如果之前持有其他引用，应该先释放
                        release();
                        ptr=cur.ptr,count=cur.count;
                        if(count)++(*count);
                    }
                    return *this;            
                }
                void release(){
                    if(count&& !--(*count)){
                        delete ptr;
                        delete count;
                    }
                }
                T operator*(){return *ptr;}
                T* operator->(){return ptr;} 
                T* get(){ return ptr; }
                int use_count(){return count?*count:0;}
        };
        ```


#### new-delete
- **自由存储区** ：C++通过new和delete来动态分配和释放对象的抽象内存区域
    - 一般编译器会用堆来实现，即使用malloc/free来实现`operator new`/`operator delete`

- `operator new`与`new operator`
    - `operator new` ：运算符函数`void* operator new(std::size_t)`
        - cpp用于分配指定字节内存的函数（**只负责内存分配**）。成功返回指向内存的指针，分配失败会抛出异常`std::bad_alloc`
        - 使用`operator new`分配的内存必须使用`operator delete`释放，因为使用`delete`等于使用`operator delete`+调用析构函数
        - 布局new(`placement new`) ：对`operator new`的一种特殊重载，即`void* operator new(std::size_t, void* __p){return __p;}`
            - 该方法用于使用**已存在的内存**来初始化对象 ：默认的new是分配内存后返回指向该内存的指针。而该方法接收现有内存的指针`__p`并直接返回该指针
            - 直接调用该方法是没有意义的，因为没有调用构造函数 ：程序员是无法直接调用构造函数的，只能通过`new`关键字等方式触发。
                - 比如new关键字的特殊语法 ：`MyClass* p=new(ptr)MyClass(arg);`。即指定了指向现有内存的指针
                ```cpp
                    void* ptr = operator new(sizeof(MyClass));
                    //下述代码为编译器对MyClass* p=new(ptr)MyClass(arg);的解析
                    MyClass* p= static_cast<MyClass*>(operator new(sizeof(MyClass),ptr));
                    //把p作为this指针，调用构造函数对p指向的内存初始化
                    p->MyClass::MyClass(arg);//
                    return p;
                ```
    - `new operator` ：即我们的new关键字，实现上会先调用`operator new`分配对象内存，再对这片内存调用构造函数初始化（实现方式类似上面代码）

- new和malloc的异同
    - new不止会进行分配内存(`operator new`)，还会再调用对象的构造函数进行初始化；delete时先调用析构函数，再释放内存
        - 如果是new数组`new int[num]`，则释放时应使用`delete[]`确保对每个元素都调用析构函数
    - new和malloc都支持延迟分配内存，即先申请，访问时（比如初始化）再分配内存页
        - new失败抛出异常`std::bad_alloc`
        - malloc失败返回NULL
    - delete只能删除new分配，free只能删除malloc分配

### cpp的编译模型
> C++ 的编译模型可以分为三个主要阶段：**预处理（Preprocessing）**、**编译（Compilation）**和**链接（Linking）**。这个过程将源代码文件（`.cpp`）转换成最终的可执行程序。

1. 预处理 (Preprocessing) ：预处理器（preprocessor）会处理以 `#` 开头的指令
    - 将`#include`指定的头文件内容复制到当前文件
    - 将`#define`的宏定义进行文本替换
    - 处理`#if` / `#ifdef`等条件编译指令，决定保留/忽略哪些代码块

1. 编译 (Compilation)
    - 前端 ：负责理解和分析源代码，并对代码进行优化
        1. **词法分析(Lexical Analysis)** ：从源代码读取字符流，并将其分解成有意义的**词法单元（Tokens）**
        1. **语法分析 (Syntactic Analysis)** ：根据语言的语法规则，将Tokens流构建成**抽象语法树（Abstract Syntax Tree, AST）**
            - 用于检查代码的结构是否符合语法规则，不满足则无法
        1. **语义分析 (Semantic Analysis)** ：检查 AST 的**语义**的正确性（对ast进行类型检查、声明检查、作用域确认等）
    - 中间代码生成（Intermediate Code Generate）：将AST树转换为三地址码之类的中间表示（Intermediate Representation, IR）
    - 后端 ：将IR翻译为目标机器的汇编代码，再把汇编代码转为机器码，输出**目标文件（Object File）**

1. 链接 (Linking) ：链接器（linker）将所有**目标文件**和所需的**库文件**（包括静态库和动态库）连接在一起，为所有函数和变量分配最终的内存地址，并把目标文件的外部引用替换为实际的内存地址。最终输出一个可执行文件
    - 链接静态库会把所需函数/变量的具体代码从静态库复制到可执行文件，运行时不再需要依赖静态库
    - 链接动态库会将库的相关信息记录到可执行文件。运行时os会将需要的动态库代码加载并链接到程序

### STL库
#### vector ：动态数组（通过静态数组+扩容机制实现）
- 扩容机制
    - 内部会维护当前元素数量`size()`和容器容量大小`capacity()`
    - 当`size`超过`capacity`时，会触发扩容 ：申请一片更大的内存 ：如果元素实现了移动构造并标识为`noexcept`则使用移动构造，否则调用元素的拷贝构造
    - 可以通过`reserve()`预指定容量大小，当容量发生变化时，vector原本的迭代器都会失效
    - 当删除某一元素，该元素及其之后的迭代器也都会失效
- push_back与emplace_back
    - push_back(T& x) ：接收一个已存在对象,通过该对象进行拷贝/移动构造函数
    - empalce_back(Args&&... args) ：接收构造元素的参数并在vector内部构造元素

- vector的简单实现

    ```cpp
    #include<iostream>

    template<class T>
    class MyVector{
        private:
        T* begin = nullptr;
        T* end = nullptr;
        T* capacity = nullptr;

        public:
        template<class... Args>
        void emplace_back(Args&&... args){
            if(end==capacity)reserve(capacity==begin?1:(capacity-begin)<<1);
            new(end++)T(std::forward<Args>(args)...);
        }
        void pop_back(){
            destroy(--end);
        }
        size_t size(){return end-begin}
        void clear(){
            while(end!=begin)destroy(--end);
        }
        void reserve(size_t n){
            if(n<=capacity-begin)return;
            T* new_begin = allocate(n);
            for(T* p=begin, *np=new_begin;p!=end;++p,np++)construct(np,std::move(*p));
            size_t sz=end-begin;
            clear();
            deallocate();
            begin=new_begin,end=begin+sz,capacity=begin+n;
        }

        MyVector(size_t n=0){
            if(n<=0)return;
            begin=end=allocate(n);
            capacity=begin+n;
        }
        ~MyVector(){
            clear();
            deallocate();
            begin=end=capacity=nullptr;
        }

        T& operator[](size_t index){return begin[index];}

        private:
        //内存的分配/释放
        T* allocate(size_t n){
            if(!n)return nullptr;
            void* ptr = ::operator new(n*sizeof(T));
            return static_cast<T*>(ptr);
        }
        void deallocate(){
            if(!begin)return;
            ::operator delete(begin);
        }
        
        //元素的构建/销毁
        template<class... Args>//使用可变参数模板+万能引用接收传入的构造参数，再使用完美转发调用类型T相应的构造函数
        void construct(T* p, Args&&... args){
            new(p)T(std::forward<Args>(args)...);//使用placement new 使用现有内存p进行就地构造，
        }
        void destroy(T* p){
            p->~T();
        }
    };
    ```


### 参考文章
[C++ 模版函数重载匹配规则](https://frezcirno.github.io/2025/03/03/cpp-template-matching/)  
[【C++拾遗】 从内存布局看C++虚继承的实现原理](https://blog.csdn.net/xiejingfa/article/details/48028491)  
[编程指北-cpp](https://csguide.cn/cpp/)  
[std::enable_shared_from_this原理浅析](https://0cch.com/2020/08/05/something-about-enable_shared_from_this/)  
[C++ 中 new 操作符内幕：new operator、operator new、placement new ](https://www.cnblogs.com/slgkaifa/p/6887887.html)  
