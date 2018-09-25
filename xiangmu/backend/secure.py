# -*- coding:utf-8 -*-
'''装饰器函数'''

from functools import wraps
from flask import session, redirect, url_for


def login_required(func):
    '''判断用户是否登录'''
    @wraps(func)
    def function_decrated(*args,**kwargs):
        not_in_s = 'user' not in session or session['user'] is None
        if not_in_s:
            return redirect(url_for('view_login'))
        return func(*args,**kwargs)
    return function_decrated