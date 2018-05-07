from flask import  Flask, render_template, request, send_file, url_for, session, redirect,send_from_directory
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import json

import os
from datetime import datetime
from werkzeug import secure_filename



##new

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
##end


app = Flask(__name__)
app.secret_key = '\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'
con = sqlite3.connect('database.db')
print ("Opened database successfully");
cursor = con.cursor()


@app.route('/')
def home_page():
    if session.get('username'):
        user = {'link': '/profile', 'name': session['username']}
        return render_template('home.html', user=user)
    else:
        return redirect('/login')


@app.route("/comment/", methods=["POST"])
def comment():
    if session.get('username'):
        text = request.form.get('text')
        id = request.form.get('id')
        cursor.execute('insert into comment(comment, user, item) values("%s", "%s", %s)'
                       % (text, session['username'], id))
        con.commit()
        return redirect('detail?id=' + id)


@app.route("/item-detail/", methods=["GET"])
def item_detail():
    if session.get('username'):
        id = request.args.get('id')
        cursor.execute('select name, provider, detail, isfind, id from item where id=%s' % id)
        detail = cursor.fetchone()
        detail = list(detail)
        cursor.execute('select contact from user where name="%s"' % detail[1])
        detail.append(cursor.fetchone()[0])
        cursor.execute('select comment, user from comment where item=%s order by time desc' % id)
        comments = cursor.fetchall()
        user = {'link': '/profile', 'name': session['username']}
        return render_template('item-detail.html', user=user, detail=detail, comments=comments)
    else:
        return redirect('/login')


@app.route("/found", methods=["POST", "GET"])
def found():
    if request.method == 'POST':
        if not session['username']:
            return redirect('/login')
        if (not request.form.get('name')) or (not request.form.get('detail')):
            return redirect('/found')
        cursor.execute('insert into item '
                       '(name, kind, provider, detail, isfind, isfinish)'
                       ' values("%s", "%s", "%s", "%s", 1, 0)'
                       % (request.form.get('name'), request.form.get('kind'),
                          session['username'],
                          request.form.get('detail')))
        con.commit()
        return redirect('/lost')
    else:
        if not session['username']:
            return redirect('/login')
        cursor.execute('select name, kind, provider, id from item where isfind=1 and isfinish=0')
        items = cursor.fetchall()
        user = {'link': '/profile', 'name': session['username']}
        return render_template('found.html', user=user, items=items)


@app.route("/lost", methods=["POST", "GET"])
def lost():
    if request.method == 'POST':
        if (not request.form.get('name')) \
                or (not request.form.get('detail')):
            return redirect('/found')
        cursor.execute('insert into item '
                    '(name, kind, provider, detail, isfind, isfinish)'
                    'values("%s", "%s", "%s", "%s", 0, 0)' %
                    (request.form.get('name'), request.form.get('kind'),
                        session['username'],
                        request.form.get('detail')))
        con.commit()
        return redirect('/found')
    else:
        if not session.get('username'):
            return redirect('/login')
        cursor.execute('select name, kind, provider, id from item where isfind=0 and isfinish=0')
        items = cursor.fetchall()
        user = {'link': '/profile', 'name': session['username']}
        return render_template('lost.html', user=user, items=items)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        cursor.execute('select * from user')
        user = cursor.fetchall()
        username = [n[0] for n in user]
        if request.form.get('username') in username:
            if request.form.get('password') == user[username.index(
                    request.form.get('username'))][1]:
                session['username'] = request.form.get('username')
                session['password'] = request.form.get('password')
                return redirect('/')
            else:
                return 'WRONG PASSWORD'
        else:
            return 'YOU HAVE NOT REGISTED'
    else:
        return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect('/')


@app.route("/regist/", methods=["POST"])
def regist():
    if request.method == 'POST':
        print(request.form)
        ##如果输入用户名、密码不为空，
        if len(cursor.fetchall()):
                return 'username has been registrated'
        if request.form.get('username') != '' \
                and request.form.get('password') != '':
##            cursor.execute('select from user where name="%s"' % request.form.get('username'))

            cursor.execute('insert into user '
                           '(name, password) '
                           'values("%s", "%s")'
                           % (request.form.get('username'),
                              request.form.get('password')))


            print("Successfully insert")
            con.commit()

            return redirect('/login')
        else:
            return 'ERROR NAME OR PASSWORD'


@app.route("/profile", methods=["POST", "GET"])
def profile():
    if request.method == 'POST':
        if request.form.get('password'):
            cursor.execute('update user set password="%s" where name="%s"' %
                           (request.form.get('password'), session['username']))
        cursor.execute('update user set contact="%s" where name="%s"' %
                       (request.form.get('contact'), session['username']))
        con.commit()
        return redirect('/profile')
    else:
        if not session.get('username'):
            return redirect('/login')
        cursor.execute('select * from user')
        user = cursor.fetchall()
        username = [u[0] for u in user]
        if session['username'] in username:
            contact = user[username.index(session['username'])][2]
        user = {
            'found': [],
            'lost': [],
            'name': session['username'],
            'contact': contact
        }
        cursor.execute('select name, time, id from item where isfind=0 and provider="%s"' % session['username'])
        items = cursor.fetchall()
        cursor.execute('select name, time, id from item where isfind=1 and provider="%s"' % session['username'])
        notitems = cursor.fetchall()
        return render_template('profile.html', user=user, items=items, notitems = notitems)






def init():
    cursor.execute('create table if not exists user'
                   '(name varchar(20) primary key, '
                   'password varchar(32), '
                   'contact text)')
    cursor.execute('create table if not exists item'
                   '(id integer primary key, '
                   'name varchar(20), '
                   'kind text, '
                   'provider varchar(20), '
                   'isfind integer, '
                   'isfinish integer, '
                   'detail text, '
                   'time timestamp default current_timestamp)')
    cursor.execute('create table if not exists comment'
                   '(id integer primary key, '
                   'user varchar(20), '
                   'comment text, '
                   'time timestamp default current_timestamp, '
                   'item integer, '
                   'foreign key(item) references item(id))')
    con.commit()







if __name__ == '__main__':
    init()
    app.run(port=8080)
