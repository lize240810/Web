# -*- coding:utf-8 -*-
'''程序主入口'''
from . import app
from .database import db,config
from. import views

def start_server():
    # 数据库创建
    db.create_all()
    # 配置session
    app.config['SECRET_KEY'] = 'asdasda'
    app.run(**config.RUN_CFG)
    