# -*- coding:utf-8 -*-
'''设置'''
import os 
# 配置数据库创建的的路径
DATABASE_URI = 'sqlite:///{0}'.format(os.path.join(os.environ['PROJ_PATH'],'data.db3'))
RUN_CFG = {
    'host': '0.0.0.0',
    'port': '8989',
    'debug': True
}
