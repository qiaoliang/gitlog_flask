#!/usr/bin/env python3
from flask import Flask, jsonify
from flask_cors import CORS
from parser import logParser
from repo import db
from repo.revmode import Base
import os
class FlaskSiteConfig(object):
    """默认配置"""
    GITLOG_FILE = None
    print(os.getenv('FLASK_ENV'))
    if(os.getenv('FLASK_ENV')=='production'):
        GITLOG_FILE = './prod_gitlog.txt'
    else:
        GITLOG_FILE = './test_gitlog.txt'

def create_flask_app(config):
    app = Flask(__name__,
                static_url_path="/s",           # -> 设定：要通过 /s 找到网站的静态文件
                static_folder="static",         # -> 设定：在 static 目录下存储静态资源
                template_folder="templates")    # -> 设定：在 templates 目录下存储静态资源

    app.config.from_object(config)  # -> 设定：从配置类 Config 中读取配置信息
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    return app

app = create_flask_app(FlaskSiteConfig)


@app.before_first_request
def create_tables():
    Base.metadata.create_all(db.engine())
    ris = logParser.parseLog(app.config['GITLOG_FILE'])
    db.saveRev(ris)


@app.route('/')
def route_map():
    return 'Hello World!'


@app.route('/rev')
def rev():
    rev = db.getAllRevId()
    return jsonify(revisions=rev)


@app.route('/file/<name>')
def changed_file(name):
    result = db.getRevInfosForFile(name)
    return jsonify(revisions = result)

@app.route('/files')
def changed_files():
    files = {}
    files['added'] = db.getAppendedFiles()
    files['delelted'] = db.getDeletedFiles()
    files['renamed'] = db.getRenamedFiles()
    files['modified'] = db.getModifiedFiles()
    return jsonify(files=files)

@app.route('/addedfiles')
def added_files():
    return jsonify(db.getAppendedFiles())

@app.route('/revinfo/<revid>')
def get_revInfo(revid):
    revInfo = db.getRevInfoByRevId(revid)
    return jsonify(revInfo.dict())