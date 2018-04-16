# coding: utf-8
import shelve
from flask import Flask, request, render_template, redirect, escape, Markup
import datetime
app = Flask(__name__)
DATA_FILE = 'guestbook.dat'


def save_data(name, comment, create_at):
    # 保存提交的数据
    # 通过shelve 模块打开数据库文件
    database = shelve.open(DATA_FILE)
    # 如果数据库中没有greeting_list，就新建一个表
    if 'greeting_list' not in database:
        greeting_list = []
    else:
        # 从数据库获取数据
        greeting_list = database['greeting_list']
    # 将提交的数据添加到表头
    greeting_list.insert(0, {
        'name': name,
        'comment': comment,
        'create_at': create_at,
    })
    # 更新数据库
    database['greeting_list'] = greeting_list
    # 关闭数据库文件
    database.close()


def load_data():
    # 返回已提交的数据
    # 通过shelve 模块打开数据库文件
    database = shelve.open(DATA_FILE)
    # 返回greeting_list。如果没有数据则返回空表
    greeting_list = database.get('greeting_list', [])
    database.close()
    return greeting_list


@app.route('/')
def index():
    greeting_list = load_data()
    return render_template('index.html', greeting_list=greeting_list)


@app.route('/error')
def error():
    return render_template('error.html')


@app.route('/post', methods=['post'])
def post():
    # 获取已提交的数据
    name = request.form.get('name')  # 名字
    comment = request.form.get('comment')  # 留言
    create_at = datetime.datetime.now()  # 投稿时间（当前时间）
    if (name or comment) == '':
        return redirect('/error')
    else:
        # 保存数据
        save_data(name, comment, create_at)
        # 保存后重定向到首页
        print (name, comment)
        return redirect('/')


@app.template_filter('nl2br')
def nl2br_filter(s):
    # 将换行符置换为br 标签的模板过滤器
    return escape(s).replace('\n', Markup('<br>'))


@app.template_filter('datetime_fmt')
def datetime_fmt_filter(dt):
    # 使datetime 对象更容易分辨的模板过滤器
    return dt.strftime('%Y/%m/%d %H:%M:%S')


if __name__ == '__main__':
    app.run('127.0.0.1', 8000, debug=True)
