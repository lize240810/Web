# -*- coding:utf-8 -*-
'''
    视图模块类
'''
import json

from flask import (
    session,
    request,
    url_for,
    render_template,
    render_template_string,
    redirect,
    flash
    )
from sqlalchemy.sql import and_ as sql_and

from . import app
from . import utils
from .database import db, User, User_folder
from .secure import login_required

@app.route(r'/', methods=['GET'])
@login_required
def view_index():
    return render_template('index.html')

@app.route('/empty')
@login_required
def view_empty():
    ''' 主界面_视图'''
    temp_str = '''这里是主界面 {{ session.get('user') }} <hr/><a href="{{ url_for('view_logout') }}">注 销</a>'''

@app.route(r'/login',methods=['POST','GET'])
def view_login():
    '''登录界面_视图'''
    # 判断session中是否存在用户
    in_s = 'user' in session and not session['user'] is None
    # 存在就跳转到主界面
    if in_s:
        return redirect(url_for('view_index'))

    # 判断登录方式
    if request.method == 'POST':
        # 获取参数
        req_username = request.values.get('username', None)
        req_password = request.values.get('password', None)
        # 判断参数是否非空
        if not req_username is None or not req_password is None:
            _username = req_username.strip() # 去除空格
            _password = req_password.strip() # 去除空格
            if bool(_username):
                if not bool(_password):
                    flash('缺少密码')
                else:
                    # 连接数据库查询用户信息
                    cursor = User.query.filter(sql_and( # 查询
                        User.username == _username, # 设置参数
                        User.password == utils.calc_md5(_password), # 设置密码
                        ))
                    print(cursor.count())
                    if cursor.count() > 0:
                        # 保存session用户名
                        user_obj = cursor.first()
                        # 设置session（注意：session值不能使User对象，需要是Python内置类型）
                        session['user'] = user_obj.to_dict()
                        return redirect(url_for('view_index'))
                    else:
                        flash('用户名或密码不正确')
            else:
                flash('用户名不正确')
        else:
            flash('用户名不允许为空')
    return render_template('login1.html')

@app.route(r'/logout')
@login_required
def view_logout():
    '''用户注销'''
    session.pop('user',None)
    return render_template('login1.html')

@app.route(r'/ajax-user-folder-list', methods=['GET', 'POST'])
def view_user_folder_list():
    '''用户文件夹数据展示'''
    # 从session中获取用户
    s_user = session['user']
    # 获取请求路径
    req_path = request.values.get('path', None)
    # 判断设置值
    if (not bool(req_path)) or req_path == "/":
        req_path = None

    # 查询文件列表（user_folder对象）
    uf_list = User_folder.list_by_path(s_user['_id'], req_path)

    # 把查询到的文件列表转换为内置数据对象dict
    uf_list = list(map(lambda item: item.to_dict(), uf_list))
    # 转换为json 返回字符串
    return json.dumps(uf_list, ensure_ascii=False)


