#!/usr/bin/env python3
from flask import Flask
from flask_cors import CORS
from parser import logParser

class FlaskSiteConfig(object):
    """默认配置"""
    GITLOG_FILE ='./1.txt'

def create_flask_app(config):

    app = Flask(__name__,
        static_url_path="/s",           # -> 设定：要通过 /s 找到网站的静态文件
        static_folder="static",         # -> 设定：在 static 目录下存储静态资源
        template_folder="templates")    # -> 设定：在 templates 目录下存储静态资源

    app.config.from_object(config) # -> 设定：从配置类 Config 中读取配置信息
    """
    CORS(app, origins=None, methods=None, supports_credentials=False)

    origins: 允许来自的来源或原始列表。原点可以是正则表达式，区分大小写的字符串，也可以是星号.
    允许来源用于非简单请求的方法或方法列表。类似于django中的CORS_ORIGIN_REGEX_WHITELIST；
    methods: 跨域请求允许的请求方法,相当于django中的CORS_ALLOW_METHODS；
    supports_credentials: 为True，允许用户进行经过身份验证的请求。允许跨域提交cookie。
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})  
    return app
app = create_flask_app(FlaskSiteConfig)

@app.route('/') 
def route_map():
    return 'Hello World!'

@app.route('/logfile') 
def logfile():
    return logParser.get_contends(app.config['GITLOG_FILE'])
