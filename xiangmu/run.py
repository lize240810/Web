# -*- coding:utf-8 -*-
'''程序运行入口'''
import os
# 一、获取程序运行的路径
os.environ['PROJ_PATH'] = os.getcwd()

from backend.main import start_server

if __name__ == '__main__':
    start_server()
    
