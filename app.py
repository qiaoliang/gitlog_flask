#!/usr/bin/env python3
from flask import Flask, Blueprint, request, redirect,session,render_template, jsonify, make_response,abort,g
import json
from werkzeug.routing import BaseConverter

class FlaskSiteConfig(object):
    """默认配置"""
    GITLOGFILE ='1.txt'

def create_flask_app(config):

    app = Flask(__name__,
        static_url_path="/s",           # -> 设定：要通过 /s 找到网站的静态文件
        static_folder="static",         # -> 设定：在 static 目录下存储静态资源
        template_folder="templates")    # -> 设定：在 templates 目录下存储静态资源

    app.config.from_object(config) # -> 设定：从配置类 Config 中读取配置信息    
    return app

app = create_flask_app(FlaskSiteConfig)

@app.route('/') 
def route_map():
    return 'Hello World!'
