# -*- coding: utf-8 -*-
'''
开发阶段-初始化数据
'''
import os
# 设置环境变量PROJ_ROOT
os.environ['PROJ_PATH'] = os.getcwd()

from backend.utils import calc_md5
from backend.database import db, User, User_folder


def init_user():
    '''初始化用户（确保至少有一个[原始]用户）'''
    cursor = User.query
    if cursor.count() < 1:
        # 创建用户的同时,把密码进行md5加密
        usr = User(username='lisi', password=calc_md5('123456'))
        # 添加到数据库中
        db.session.add(usr)
        # 提交数据
        db.session.commit()
        print(usr.to_dict())
    else:
        print('用户已存在:')
        print(cursor.first().to_dict())

def add_folder():
    '''文件夹表添加数据'''
    # 1.获取用户id(外键) first 获取第一个
    u = User.query.first() # 查询数据
    # 2.实例化用户文件夹类
    #  None为跟目录 /
    uf = User_folder(None, u._id)
    # 添加一个数据
    db.session.add(uf)
    db.session.add(User_folder('/home', u._id))
    db.session.add(User_folder('/home/zhangsan', u._id))
    db.session.add(User_folder('/home/lisi', u._id))
    db.session.add(User_folder('/home/lisi/python', u._id))
    db.session.add(User_folder('/home/lisi/3', u._id))
    db.session.add(User_folder('/home/lisi/2', u._id))
    db.session.add(User_folder('/home/lisi/java', u._id))
    db.session.add(User_folder('/root', u._id))
    db.session.commit()

if __name__ == '__main__':
    # 确保数据库存在
    db.create_all()
    # 添加初始用户
    init_user()
    add_folder()