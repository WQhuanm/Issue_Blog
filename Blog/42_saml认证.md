---
title: saml认证
date: 2025-07-12 17:34:26
mathjax: true
categories: 
    - CS基础
tags: 
    - CS基础
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202507130124543.png
---


### saml的作用
1. 全称是Security Assertion Markup Language：安全访问标记语言，基于xml标准
1. saml常用于SSO(单点登录)：用户在IDP(Identity Provider，身份鉴别服务器)认证后，经过saml流程会获取到认证凭证（比如cookie），认证凭证有效期内，访问SP(Service Providers，服务提供者)无需重复登录
1. SAML协议的核心是: IDP和SP通过用户的浏览器的请求来实现交换数据（IDP和SP一般不直接进行数据交换）
    + sp，idp通过浏览器向另一方传递samlRequest或samlResponse（加密的xml文档信息），最终达到认证的目的

### saml认证流程
1. 用户访问SP需要认证的资源时，SP会检查请求是否携带标识认证的cookie("AUTH")
1. 不存在，SP会生成请求参数samlRequest（用于微软对用户认证）和RelayState（用于认证成功后重定向会原本的请求链接），将请求重定向到Idp进行认证
1. 浏览器在Idp成功登录后，会执行成功登录页面的js脚本，生成请求参数samlResponse（用于SP解析用户详细），并携带之前的RelayState参数，向SP发送成功认证请求
1. SP把samlResponse成功解析后会生成认证cookie("AUTH")签发给用户，并跳转到原本的请求页面
1. 以后用户访问，只需解析这个cookie的信息即可
