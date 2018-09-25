import os


from flask import Flask


# 二、创建flask对象
app = Flask(
    __name__,
    static_folder = os.path.join(os.environ['PROJ_PATH'], 'frontend', 'static'),
    template_folder = os.path.join(os.environ['PROJ_PATH'], 'frontend', 'templates')
    )

