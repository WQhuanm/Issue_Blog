---
title: Mybatis编码随记
date: 2025-02-19 08:55:41
categories: 
    - MyBatis
tags: 
    - MyBatis
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202502191654445.png
---

###  1. #{} 和 ${} 区别
+ #{}: 解析为SQL时，会将形参变量的值取出，并自动给其添加引号。该方式预编译后在把内容填入，预防SQL注入
+ ${}: 解析为SQL时，将形参变量的值直接取出，直接拼接显示在SQL中,该方式是拼接后再进行sql编译，存在安全隐患

### 2. Mybatis映射器<mappers>
#### insert主键自增
``` xml
<!-- useGeneratedKeys="true" keyProperty="id" 指定id为主键并启用自增-->
<insert id="唯一标识" useGeneratedKeys="true"
    keyProperty="id">
  insert into Author (username,password,email,bio)
  values (#{username},#{password},#{email},#{bio})
</insert>
```
##### 
#### resultMap
1. 联表查询的结果一般使用resultType="map"映射或者定义resultMap来映射
2. resultMap有嵌套/分步查询与单步查询，因避免使用分步查询以防止出现"N+1查询问题"
``` xml
<resultMap id="该元素的唯一标识" type="POJO类">
    <id property="POJO属性" column="DB的列名/别名" jdbcType="" javaType="除HashMap均可省略"/> <!--主键 ,ID要求标注以预防错误-->
    <result/><!--属性同id,注入到字段或JavaBean属性的普通结果 -->
    <association property="studentcard" resultMap="可选择引用map，或标签内映射id/result标签"></association><!-- 用于一对一关联 -->
    <collection property="" ofType="指定集合元素的POJO类" >
        <id />
        <result />
    </collection><!-- 用于一对多、多对多关联 -->
</resultMap>
```

### 3. 动态SQL
#### if标签：条件判断
```xml
<if test="判断条件为真执行">
    SQL语句
</if>
```
#### choose、when和otherwise标签（switch-case-default）
```xml
<choose>
    <when test="判断条件1">
        SQL语句1
    </when>
    <when test="判断条件2">
        SQL语句2
    </when>
    <otherwise>
        SQL语句3
    </otherwise>
</choose>
```
#### trim,where,set标签 ：字符串拼接
```xml
<trim prefix="添加前缀" suffix="添加后缀" prefixOverrides="忽略前缀字符" suffixOverrides="忽略后缀字符">
    SQL语句
</trim>

<!-- 等价<where></where> -->
<trim prefix="WHERE" prefixOverrides="AND |OR ">
  ...
</trim>

<!-- 等价set<set></set> -->
<trim prefix="SET" suffixOverrides=",">
  ...
</trim>

```
#### foreach标签
对集合进行遍历（尤其是在构建 IN 条件语句的时候）
```xml
SELECT *
FROM POST P
WHERE ID in
<!-- item为值(value)，index为集合下标/key -->
<foreach item="item" index="index" collection="list|array|map|set的集合之一" open="(" separator="," close=")">
    参数值
</foreach>
```




