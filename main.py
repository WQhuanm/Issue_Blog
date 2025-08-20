# -*- coding: utf-8 -*-
import argparse
import os
import re
import markdown
from feedgen.feed import FeedGenerator
from github import Github
from lxml.etree import CDATA
from marko.ext.gfm import gfm as marko

MD_HEAD = """## [前往我的博客](https://wqhuanm.github.io/Issue_Blog/)
如果你想部署类似的博客网站，可以参考我的这篇[blog](https://github.com/WQhuanm/Issue_Blog/issues/2)
"""

BACKUP_DIR = "Blog" #存放issue的博客，用来部署到静态网站
README_DIR = "README.md" #README路径

ANCHOR_NUMBER = 5
TOP_ISSUES = "Top"
TODO_ISSUES = "TODO"
FRIENDS_LABELS = "Friends"
ABOUT_LABELS = "About"
IGNORE_LABELS = [ TOP_ISSUES , TODO_ISSUES , FRIENDS_LABELS , ABOUT_LABELS]

FRIENDS_TABLE_HEAD = "| Name | Link | Desc | \n | ---- | ---- | ---- |\n"
FRIENDS_TABLE_TEMPLATE = "| {name} | {link} | {desc} |\n"
FRIENDS_INFO_DICT = {
    "名字": "",
    "链接": "",
    "描述": "",
}


def is_me(issue, me):
    return issue.user.login == me
def is_hearted_by_me(comment, me):
    reactions = list(comment.get_reactions())
    for r in reactions:
        if r.content == "heart" and r.user.login == me:
            return True
    return False
def format_time(time):
    return str(time)[:10]

def parse_TODO(issue):
    body = issue.body.splitlines()
    todo_undone = [l for l in body if l.startswith("- [ ] ")]
    todo_done = [l for l in body if l.startswith("- [x] ")]
    # just add info all done
    if not todo_undone:
        return f"[{issue.title}]({issue.html_url}) all done", []
    return (
        f"[{issue.title}]({issue.html_url})--{len(todo_undone)} jobs to do--{len(todo_done)} jobs done",
        todo_done + todo_undone,
    )


def get_issues_from_milestone(repo, milestone_title):
    target_milestone = None
    for milestone in repo.get_milestones(state='open'):
            if milestone.title == milestone_title:
                target_milestone = milestone
                break
    return repo.get_issues(milestone=target_milestone)

def add_issues_info(title, issues, md_dir,me,limit=ANCHOR_NUMBER):
    if not issues:
        return
    with open(md_dir, "a+", encoding="utf-8") as md:
        md.write(title)
        for issue in issues:
            if not is_me(issue, me):
                continue
            limit -= 1
            if limit == -1:
                md.write("<details><summary>显示更多</summary>\n\n")
            time = format_time(issue.created_at)
            md.write(f"- [{issue.title}]({issue.html_url})--{time}\n")
            
        if limit <= 0:
            md.write("</details>\n")
        md.write("\n\n")

# normal md
def add_md_header(md_dir, repo_name):
    with open(md_dir, "w", encoding="utf-8") as md:
        md.write(MD_HEAD.format(repo_name=repo_name))
        md.write("\n")

def add_md_todo(repo, md_dir, me):
    todo_issues = list(repo.get_issues(labels=TODO_ISSUES))
    if not todo_issues:
        return
    with open(md_dir, "a+", encoding="utf-8") as md:
        md.write("## TODO\n")
        for issue in todo_issues:
            if is_me(issue, me):
                todo_title, todo_list = parse_TODO(issue)
                md.write("TODO list from " + todo_title + "\n")
                for t in todo_list:
                    md.write(t + "\n")
                md.write("\n")
                
def add_md_top(repo, md_dir, me):
    title = "## 置顶文章\n"
    top_issues = list(get_issues_from_milestone(repo,TOP_ISSUES))
    add_issues_info(title, top_issues, md_dir, me)

def add_md_recent(repo, md_dir, me, limit = ANCHOR_NUMBER):
    title = "## 最近更新\n"
    issues = list(repo.get_issues())
    add_issues_info(title, issues, md_dir, me, limit)

def add_md_milestone(repo, md_dir, me):
    milestones = repo.get_milestones(state='open')
    # sort milestones by description info if it exists (eg: let description start with number), otherwise sort by name,
    milestones = sorted(
        milestones,
        key=lambda x: (
            x.description is None,
            x.description == "",
            x.description,
            x.title,
        ),
    )

    for milestone in milestones:
        if milestone.title in IGNORE_LABELS:
            continue
        title = f"## {milestone.title}\n"
        issues = list(get_issues_from_milestone(repo,milestone.title))
        add_issues_info(title, issues, md_dir, me)

# md_friends
def _make_friend_table_string(s):
    info_dict = FRIENDS_INFO_DICT.copy()
    try:
        string_list = s.splitlines()
        # drop empty line
        string_list = [l for l in string_list if l and not l.isspace()]
        for l in string_list:
            string_info_list = re.split("：", l)
            if len(string_info_list) < 2:
                continue
            info_dict[string_info_list[0]] = string_info_list[1]
        return FRIENDS_TABLE_TEMPLATE.format(
            name=info_dict["名字"], link=info_dict["链接"], desc=info_dict["描述"]
        )
    except Exception as e:
        print(str(e))
        return
def add_md_firends(repo, md_dir, me):
    s = FRIENDS_TABLE_HEAD
    friends_issues = list(repo.get_issues(labels=FRIENDS_LABELS))
    if not FRIENDS_LABELS or not friends_issues:
        return
    friends_issue_number = friends_issues[0].number
    for issue in friends_issues:
        for comment in issue.get_comments():
            if is_hearted_by_me(comment, me):
                try:
                    s += _make_friend_table_string(comment.body or "")
                except Exception as e:
                    print(str(e))
                    pass
    s = markdown.markdown(s, output_format="html", extensions=["extra"])
    with open(md_dir, "a+", encoding="utf-8") as md:
        md.write(
            f"## [友情链接](https://github.com/{str(me)}/gitblog/issues/{friends_issue_number})\n"
        )
        md.write("<details><summary>显示</summary>\n")
        md.write(s)
        md.write("</details>\n")
        md.write("\n\n")

# RSS
def _valid_xml_char_ordinal(c):# help to covert xml vaild string
    codepoint = ord(c)
    # conditions ordered by presumed frequency
    return (
        0x20 <= codepoint <= 0xD7FF
        or codepoint in (0x9, 0xA, 0xD)
        or 0xE000 <= codepoint <= 0xFFFD
        or 0x10000 <= codepoint <= 0x10FFFF
    )

def generate_rss_feed(repo, filename, me):
    generator = FeedGenerator()
    generator.id(repo.html_url)
    generator.title(f"RSS feed of {repo.owner.login}'s {repo.name}")
    generator.author(
        {"name": os.getenv("GITHUB_NAME"), "email": os.getenv("GITHUB_EMAIL")}
    )
    generator.link(href=repo.html_url)
    generator.link(
        href=f"https://raw.githubusercontent.com/{repo.full_name}/main/{filename}",
        rel="self",
    )
    for issue in repo.get_issues():
        if not issue.body or not is_me(issue, me) or issue.pull_request:
            continue
        item = generator.add_entry(order="append")
        item.id(issue.html_url)
        item.link(href=issue.html_url)
        item.title(issue.title)
        item.published(issue.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"))
        for label in issue.labels:
            item.category({"term": label.name})
        body = "".join(c for c in issue.body if _valid_xml_char_ordinal(c))
        item.content(CDATA(marko.convert(body)), type="html")
    generator.atom_file(filename)

# generate issue's md
def save_issue(issue, dir_name, me):
    md_name = os.path.join(
        dir_name, f"{issue.number}_{issue.title.replace('/', '-').replace(' ', '.')}.md"
    )
    # change issue  to md  (Hexo requires this format)
    # ---
    # title: issue.title 
    # date: issue.create_date
    # mathjax: true
    # categories:
    #     - issue.milestone
    # tags:
    #     - issue.label
    #     - issue.label
    #     .....
    # cover: image_url
    # ---
    # issue.body 
    #

    #the cover have default value,if you want to change,make sure the issue body's first line is ![](image_url) or change the following code 
    with open(md_name, "a", encoding="utf-8") as f:
        f.write("---\n")
        f.write(f"title: {issue.title}\n")
        f.write(f"date: {issue.created_at}\n")
        f.write(f"mathjax: true\n")
        if issue.milestone:
            f.write("categories: \n")
            f.write(f"    - {issue.milestone.title}\n")
        if issue.labels:
            f.write("tags: \n")
            for label in issue.labels:
                f.write(f"    - {label.name}\n")

        image_url = "https://gcore.jsdelivr.net/gh/WQhuanm/Img_repo_1@main/img/202412222015910.png" # default image url
        issue_body = issue.body
        match = re.match(r'!\[.*?\]\((https?://[^\)]+)\)', issue.body)# 使用正则表达式匹配图片链接
        if match:
            image_url = match.group(1)
            issue_body = issue.body.split('\n', 1)[1]
        f.write(f"cover: {image_url}\n")
        f.write("---\n\n")
        f.write(issue_body)

def generate_issue_md(repo, dir_name, me, issue_number=None):
    md_files = os.listdir(dir_name)
    cur_issues = [
        int(i.split("_")[0]) for i in md_files if i.split("_")[0].isdigit()
    ]
    add_issues = [
        i
        for i in list(repo.get_issues())
        if int(i.number) not in cur_issues
    ]
    if issue_number:
        add_issues.append(repo.get_issue(int(issue_number)))
    for issue in add_issues:
        save_issue(issue, dir_name, me)


def main(token, repo_name, issue_number=None, dir_name=BACKUP_DIR):
    user = Github(token)
    me = user.get_user().login
    repo = user.get_repo(repo_name)

    # add to readme one by one, change order here
    add_md_header(README_DIR, repo_name)
    for func in [add_md_todo,
                 add_md_top,
                 add_md_recent,
                 add_md_milestone,
                 add_md_firends,]:
        func(repo, README_DIR, me)

    generate_rss_feed(repo, "feed.xml", me)
    generate_issue_md(repo, dir_name, me, issue_number)

if __name__ == "__main__":
    if not os.path.exists(BACKUP_DIR):
        os.mkdir(BACKUP_DIR)
    parser = argparse.ArgumentParser()
    parser.add_argument("github_token", help="github_token")
    parser.add_argument("repo_name", help="repo_name")
    parser.add_argument(
        "--issue_number", help="issue_number", default=None, required=False
    )
    options = parser.parse_args()
    main(options.github_token, options.repo_name, options.issue_number)
