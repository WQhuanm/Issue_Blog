---
title: 使用Issue+Hexo搭建博客
date: 2024-12-23 07:46:12
mathjax: true
categories: 
    - Top
tags: 
    - Top
    - GitHub
cover: https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202412231400807.png
---

>本文主要借鉴于Github的一个issue_blog项目：[yihong0618/gitblog](https://github.com/yihong0618/gitblog)

+ 在基于以往的Hexo博客部署的基础上，使用了Github：Action来自动部署，只需要把文章提交到issue（可以使用label打标签，使用milestone来归档），其他环节交给action即可
#### 最终效果可参考
>我的[Blog仓库](https://github.com/WQhuanm/Issue_Blog)以及[Blog网站](https://wqhuanm.github.io/Issue_Blog/)

### 一，配置Blog repo：
clone这个[仓库](https://github.com/WQhuanm/Issue_Blog.git)到你想用来建立博客的仓库

这份博客运作的核心有三:

1. main.py: 内含生成readme的逻辑
2. generate_readme.yml: 通过action自动调用main.py生成readme
3. generate_page.yml: 在readme生成后，将博客部署到Gitpage网站

#### 必须执行的操作(require)
##### 1. 获取你的Github Token
[Github Token](https://github.com/settings/tokens)
      
![](https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202412231319184.png)
有效期建议无限，否则每次过期你需要重新替换。
后面权限建议全部勾选，以防workflow权限不够。
![](https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202412231340696.png)

最后Generate token便可获取，注意保存这个字符串，只会出现这一次

![](https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202412311236964.png)

##### 2. 在你博客仓库的settings的Actions secrets and variables添加你刚刚获得的token。
建议命名为G_T(否则需要把2个workflow里面的G_T改为你设定的名字)
![](https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202412231356327.png)

##### 3.在你博客仓库的settings的Actions ：General里运行workflow的读写权限
![](https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202412231359958.png)

##### 4. 删除Blog文件夹（因为里面是我博客的存档）
ps：你每次删除该文件夹，博客部署时都会检测是否有其他文章的md文件不存在，检测到则会重新生成的

#### Option
1. 更改main.py的MD_HEAD内容，这个会写在readme头部

#### 执行后上述操作，你以后每次写issue(可以打上相关的label),都会更新到readme作为一个索引目录了。
readme会根据你打的label对你的博客进行分类

### 二，配置 Github Page
我这里提供一种hexo的配置思路，采用的主题是[kira](https://github.com/ch1ny/kira-hexo)

#### 1. 你可以根据你选择的hexo主题进行本地配置后，把这个主题上传到你的私人仓库方便后面workflow来clone
 + 我也提供了一个[公共仓库](https://github.com/WQhuanm/Test_Blog_Repo.git)以便您进行测试，你可以先暂时使用这个
 + 建议**私人**仓库，因为你配置文件极可能有个人敏感信息
 + 建议先在本地测试好你的静态网站部署是成功的，然后配置成私人仓库给workflow来clone，毕竟本地调试和配置要容易的多


#### 2. 修改 .github\workflows\generate_page.yml，参考里面的注释
 + 修改BASE_URL
 + 修改name为 Generate Hexo public 任务里面的克隆仓库（也可以改成我提供的仓库来测试:https://github.com/WQhuanm/Test_Blog_Repo.git)
 
#### 3. 请把博客仓库的settings的page的生成改成使用action生成
否则GitPage的部署默认使用分支部署，呈现出来的页面即是你的readme内容
![](https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202412240007927.png)


#### 配置后，用issue写文章格式如下
+ issue的第一行如果是md的图片链接，会设定为你网站博客的头图，否则使用默认头图
+ issue打上milestone时，网站会对该文章进行分类归档
+ issue打上labels时，网站会对该文章添加tags（可有多个tag）

#### Option
+ workflow生成page时，可以使用gulp用于压缩文件，提高前端页面访问效果，方法在[我的测试仓库](https://github.com/WQhuanm/Test_Blog_Repo.git)的README.md文件有具体提及。
 
+ 如果你有很多图片上传的需求，推荐你使用国内主流图床或者使用Github做图床+CDN技术来优化，可以参考[jsDelivr和Github配合才是最佳免费CDN，五分钟学会使用，附搭建免费图床教程](https://blog.csdn.net/weixin_44786530/article/details/129851540)

#### 附注另一种方法：使用Zola简易配置Gitpage
>[yihong0618/gitblog](https://github.com/yihong0618/gitblog)使用Zola配置了Github Page。我这里简要介绍一下zola的配置

1. 你无需弄一个私有仓库了，只需要在博客仓库根目录添加一个config.toml文件，内容如下:
 ``` toml
    base_url = "https://{username}.github.io/{your blog repo}/" #如果repo是{username}.github.io,请改为https://{username}.github.io/
    generate_feeds = true
    feed_filenames = ["rss.xml"]
    theme = "even"
    taxonomies = [
        {name = "categories", feed = true},
        {name = "tags", feed = true},
    ]
    [extra]
    even_title = "yihong0618's Blog"
    even_menu = [
        {url = "$BASE_URL", name = "Home"},
        {url = "$BASE_URL/tags/top/", name = "Top"},
        {url = "$BASE_URL/issue-282/", name = "About"},
    ]
 ```

1. generate_page.yml改为这个
 ``` yml
    name: Deploy static content to GitPages
    on:
    workflow_dispatch:
    workflow_run:
        workflows: [Generate GitBlog README]  # Depends on the completion of the workflow: Generate GitBlog README
        types:
        - completed
    # Sets permissions of the GITHUB_TOKEN to allow deployment to GitHub Pages
    permissions:
    contents: read
    pages: write
    id-token: write
    concurrency:
    group: ${{ github.workflow }}
    cancel-in-progress: true
    jobs:
    deploy:
        environment:
            name: github-pages
            url: ${{ steps.deployment.outputs.page_url }}
        runs-on: ubuntu-latest
        env:
            GH_TOKEN: ${{ github.token }}
            ISITE_VERSION: v0.1.3
            ZOLA_VERSION: v0.19.2
            USER: ${{ github.repository_owner }}
            REPO: ${{ github.event.repository.name }}
             #if you use Gitpage and your repo'name is not {usernmae}.github.io,please use this
            BASE_URL: https://${{ github.repository_owner }}.github.io/${{ github.event.repository.name }}
            # else if your repo's name is {usernmae}.github.io,please use this,please use this
            # BASE_URL: https://${{ github.repository_owner }}.github.io/${{ github.event.repository.name }}
        steps:
        - name: Checkout
            uses: actions/checkout@v4
        - name: Generate markdown
            run: |
            gh release download $ISITE_VERSION --repo kemingy/isite -p '*Linux_x86_64*' --output isite.tar.gz
            tar zxf isite.tar.gz && mv isite /usr/local/bin
            isite generate --user $USER --repo $REPO
            gh release download $ZOLA_VERSION --repo getzola/zola -p '*linux*' --output zola.tar.gz
            tar zxf zola.tar.gz && mv zola /usr/local/bin
            cp config.toml output/config.toml
            cd output && zola build --base-url $BASE_URL
        - name: Setup Pages
            uses: actions/configure-pages@v4
        - name: Upload artifact
            uses: actions/upload-pages-artifact@v2
            with:
            path: 'output/public'
        - name: Deploy to GitHub Pages
            id: deployment
            uses: actions/deploy-pages@v3
 ```

### 参考文章:
[这个博客开源了](https://github.com/yihong0618/gitblog/issues/177)

[使用 GitHub Issues 来写博客，真香。](https://xie.infoq.cn/article/f89ea3ba86724ef568880ad04)

[jsDelivr和Github配合才是最佳免费CDN，五分钟学会使用，附搭建免费图床教程](https://blog.csdn.net/weixin_44786530/article/details/129851540)


[加快GitHub Pages国内访问速度](https://zu1k.com/posts/coding/speedup-github-page/#%E4%BD%BF%E7%94%A8-cdn)
