[TOC]

# python-flask-docker

该模版演示基于 Python + Flask 实现全自动检出代码 -> 单元测试 -> 构建 Docker 镜像 -> 推送到 Docker 制品库 -> 部署到远端服务器

## 文件解释

样例包括:

- README.md - 本文件。项目概述及一些说明
- Dockerfile - 用以自动构建 Docker 镜像的脚本
- requirements.txt - 依赖包文件
- app.py - 主 Flask 服务器端源代码

## 快速开始

如下这些引导，假定你想在自己的电脑上开发本项目。

1. 安装依赖

```bash
$ pip3 install -r requirements.txt
```

2. 生成 git log

```bash
$ cd {your_chromium_dir}/src
$ git log --name-status --abbrev-commit --format="Revision: %h%n###%s%n<<<<Detail:%n%b<<<<End" HEAD...{your_old_revision} > prod_gitlog.txt
$ cp prod_gitlog.txt {your_flask_app_dir}
```


3. 启动服务器

```bash
$ export FLASK_app=app
$ export FLASK_ENV=develop  # 默认是 production
$ flask run -h 127.0.0.1 -p 1313
```

4. 打开 <http://127.0.0.1:1313/> .


## 测试

生成单元测试报告/代码覆盖率报告

```
pytest --junitxml=reports/test-result.xml --cov=./ --cov-report=xml --cov-report=html --cov-report=term
```

生成代码覆盖率增量对比报告, 默认对比远端的 master 分支
 ```
diff-cover coverage.xml --compare-branch=origin/master --html-report report.html
```


