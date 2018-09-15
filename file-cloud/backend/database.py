# -*- coding:utf-8 -*-
'''数据操作'''
import re
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import and_,or_,func


from . import app
from . import config
# 三、创建数据库
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
# 不显示数据库警告
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 创建数据库对象
db = SQLAlchemy(app)

# 创建模板
class User(db.Model):
    '''用户模块'''
    __tablename__ = 'user'

    _id = db.Column('id', db.Integer, primary_key=True, autoincrement=True, comment='ID')
    username = db.Column(db.String(30), nullable=False, unique=True, comment='用户名') 
    password = db.Column(db.String(30), nullable=False, comment='密码') 

    def __init__(self, username, password):
        '''赋值操作'''
        self.username = username    
        self.password = password

    def __repr__(self):
        '''输出样式'''
        return '<{0} {1}>'.format(__class__.__name__, repr(self.username))

    def to_dict(self):
        return {
            '_id': self._id,
            'username': self.username,
            'password': self.password
        }


class File(db.Model):
    '''文件类模板'''
    __tablename__ = 'file'

    _id = db.Column('id', db.Integer, primary_key=True, autoincrement=True, comment='ID')
    md5 = db.Column(db.String(32), nullable=False, unique=True, comment='文件MD5') 
    mime_major = db.Column(db.String(16), nullable=False, comment='文件主类型')
    mime_manor = db.Column(db.String(16), nullable=False, comment='文件次类型')
    file_size = db.Column(db.Integer, nullable=False, comment='文件大小')
    store_path = db.Column(db.String(255),unique=True, nullable=False, comment='文件相对路径')
    ref_count = db.Column(db.Integer, default=1 ,nullable=False, comment='引用次数')

    def __init__(self, md5, mime_major, mime_manor, file_size, store_path, ref_count=None):
        self.mime_major = mime_major
        self.mime_manor = mime_manor
        self.file_size = file_size
        self.store_path = store_path
        if ref_count is not None:
            self.ref_count = ref_count

    def __repr__(self):
        return '<{0} {1} {2}>'.format(__class__.__name__, self.md5, self.file_size, self.ref_count)


class User_folder(db.Model):
    """用户文件夹表模板"""
    __tablename__ = 'user_folder'
    _id = db.Column('id', db.Integer, primary_key=True, autoincrement=True, comment='ID')
    path = db.Column(db.String(255), unique=True, default='/', nullable=False, comment='文件夹路径')                                            # 外键使用表名 而非模板名
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, comment='用户id')
    update_time = db.Column(db.DateTime(timezone=True), default=datetime.now, nullable=False, comment='更新时间')

    def __init__ (self, path, user_id, update_time=None):
        self.path = path        
        self.user_id = user_id
        if update_time is not None:
            self.update_time = update_time

    def __repr__ (self):
        return '<{0} {1}>'.format(__class__.__name__, repr(self.path))

    @classmethod
    def list_by_id(cls, user_id, folder_id, reverse=False):# 用户id 文件夹id
        '''根据id查询数据'''
        # 根据文件夹id查询 返回一个User_folder对象
        uf = cls.query.filter_by(_id=folder_id ).first()
        return cls.list_by_path(user_id,uf.path, reverse=reverse)

    @classmethod
    def list_by_path(cls, user_id, folder_path=None,reverse=False):
        '''根据文件夹路径获取子目录
            user_id用户id  folder_path 文件路径,reverse 排列顺序
        '''
        # 判断文件路径是否为None
        if folder_path is None:
            # 修改为""
            folder_path = ''
            # 判断文件路径/结尾
        if folder_path.endswith('/'):
            # 从第0个开始 -1个结束(切去最后的/)
            folder_path = folder_path[:-1]
            # 判断是否以文件名开头,必须有下划线
        pattern = '^{0}/[^/]+$'.format(folder_path)
        # 排列方法 根据文件名英文首字母排序 True到倒序
        sort_func = lambda item:item.path
        return sorted([
            # 待条件的查询
            uf for uf in cls.query.filter(and_(
                cls.path != None,
                cls.user_id == user_id
            ))
                if re.match(pattern, uf.path, re.I)
            ],key = sort_func, reverse=reverse)

    def to_dict(self):
        '''输出用户文件表的参数'''
        return {
            '_id':self._id,
            'path' : self.path,
            'user_id' : self.user_id,
            'update_time' : self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        }


class User_file(db.Model):
    """用户文件表"""
    __tablename__ = 'user_file'
    _id = db.Column('id', db.Integer, primary_key=True, autoincrement=True, comment='ID')
    filename = db.Column(db.String(255), nullable=False,unique=True, default='/', comment='文件名')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, comment='用户id')
    folder_id = db.Column(db.Integer, db.ForeignKey('user_folder.id'), nullable=True, comment='文件夹id')
    update_time = db.Column(db.DateTime(timezone=True), default=datetime.now , nullable=False)

    def  __init__(self,filename,user_id,folder_id,update_time=None):
        self.filename = filename
        self.user_id = user_id
        self.folder_id = folder_id
        if update_time is not None:
            self.update_time = update_time

    def __repr__(self):
        return '<{0} {1}>'.format(__class__.__name__, repr(self.filename))

class User_file_version(db.Model):
    """用户文件版本"""
    __tablename__ = 'user_file_version'

    _id = db.Column('id', db.Integer, primary_key=True, autoincrement=True, comment='ID')
    user_file_id = db.Column(db.Integer, db.ForeignKey('user_file.id'), nullable=False, comment='用户文件id' )
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False, comment='文件id')
    version = db.Column(db.Integer, default=1, nullable=False, comment='版本号')
    store_time = db.Column(db.DateTime(timezone=True), default=datetime.now ,nullable=False)

    def __init__(self, user_file_id, file_id, version, store_time):
        self.user_file_id = user_file_id
        self.file_id = file_id
        self.version = version
        if store_time is not None:
            self.store_time = store_time

    def __repr__(self):
        return '<{0} id={1}  version={2}>'.format(__class__.__name__, repr(self.user_file_id), repr(self.version))
