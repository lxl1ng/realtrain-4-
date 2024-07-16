import subprocess
import traceback

import pymysql
from flask import Flask
from flask import render_template
from flask import request
from pyqrcode import QRCode

def run_python_file(file_path):
    # 使用subprocess运行python命令来执行指定的文件
    # subprocess.run(['F:\git_repository\downloads\chatbot\venv\Scripts\python', file_path], check=True)
    subprocess.run(
            [r'F:\git_repository\downloads\chatbot\venv\Scripts\python', file_path], 
            check=True
        )

app = Flask(__name__)


# app.secret_key = '123456'

# # 数据库配置
# DATABASE_CONFIG = {
#     'host': 'localhost',
#     'user': 'your_username',
#     'password': 'your_password',
#     'database': 'mydatabase',
#     'charset': 'utf8mb4',
#     'cursorclass': pymysql.cursors.DictCursor
# }
#
#
# def get_db_connection():
#     """获取数据库连接"""
#     return pymysql.connect(**DATABASE_CONFIG)


@app.route('/')
def init():
    # 首页
    return render_template("welcome.html")


@app.route('/back_to_home')
def back_to_home():
    # 返回主页
    return render_template("welcome.html")


@app.route('/login')
def login():
    return render_template("login.html")


# 获取登录参数及处理
@app.route('/denglu') # type: ignore
def getLoginRequest():
    # 查询用户名及密码是否匹配及存在
    # 连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect(host="localhost", user="root", password="jing66127593", database="chatbot")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    sql = "select * from user where username=" + request.args.get('user') + "" # type: ignore
    try:
        # 执行sql语句
        cursor.execute(sql)
        results1 = cursor.fetchall()
        password = request.args.get('password')
        if len(results1) == 0:
            return '<script> alert("用户不存在");window.open("/login");</script>'
        if len(results1) == 1 and password != " ":
            try:
                sql = "select * from user where username=" + request.args.get(
                    'user') + " and password=" + request.args.get(# type: ignore
                    'password') + ""
                # 执行sql语句
                cursor.execute(sql)
                results2 = cursor.fetchall()
                if len(results2) == 1:
                    return '<script> alert("登录成功");window.open("http://10.242.224.108:8501");</script>'
                else:
                    return '<script> alert("密码错误");window.open("/login");</script>'
            except:
                # 如果发生错误则回滚
                traceback.print_exc()
                db.rollback()
        if len(results1) == 1 and password != " ":
            return '<script> alert("密码未填写");window.open("/login");</script>'
    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
        return '<script> alert("用户名、密码未填写");window.open("/login");</script>'
    # 关闭数据库连接
    db.close()


# 获取注册请求及处理
@app.route('/registuser')
def getRigistRequest():
    # 把用户名和密码注册到数据库中
    # 连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect(host="localhost", user="root", password="jing66127593", database="chatbot")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    sql = "select * from user where username=" + request.args.get('user') + "" # type: ignore
    # sql = "INSERT INTO user(username, password,email) VALUES (" + request.args.get('user') + ", " + request.args.get(
    #     'password') + ", " + request.args.get('email') + ")"
    username = request.args.get('user') + "" # type: ignore
    password = request.args.get('password')
    email = request.args.get('email')
    if email == " " or password == " " or username == " ":
        return '<script> alert("未填写全部内容！");window.open("/register");</script>'
    else:
        try:
            sql = "INSERT INTO user(username, password,email) VALUES (" + request.args.get(
                'user') + ", " + request.args.get( # type: ignore
                'password') + ", " + request.args.get('email') + ")"
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            # 注册成功之后跳转到登录页面
            return '<script> alert("注册成功！");window.open("/login");</script>'
        except:
            # 抛出错误信息
            traceback.print_exc()
            # 如果发生错误则回滚
            db.rollback()
            return '<script> alert("注册失败！");window.open("/register");</script>'


# WX部分
@app.route('/get_config')
def getconfig():
    config = request.args.get('config')
    if config == "glm":
        run_python_file("./app1.py")
    if config == "linkai":
        run_python_file("./app2.py")
    if config == "xunfei":
        run_python_file("./app3.py")
    return render_template("admin.html")


# 钉钉部分
@app.route('/get_config_1')
def getconfig_1():
    config_1 = request.args.get('config_1')
    if config_1 == "glm":
        run_python_file("./app4.py")
    if config_1 == "linkai":
        run_python_file("./app5.py")
    if config_1 == "xunfei":
        run_python_file("./app6.py")
    return render_template("admin_1.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/admin_1')
def admin_1():
    return render_template("admin_1.html")

if __name__ == '__main__':
    app.run(debug=False)
