# -*- coding:utf-8 -*-
'''工具函数模块'''
import hashlib

def calc_md5(msg):
    # 1.创建md5对象
    md5 = hashlib.md5()
    if isinstance(msg,str):
    # 修改参数的编码
        msg = msg.encode('utf-8', errors='ignore')
    # 计算md5
    md5.update(msg)
    return md5.hexdigest()
    
