from flask import Flask,render_template,request,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import dber
from dber import username_match as um


app=Flask(__name__)




app.config['SECRET_KEY']='1234'

secret=''
secret2=''

@app.route('/', methods=['GET','POST'])
def index():
    #create a welcome page
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    name = request.form['username']
    passw = request.form['password']
    secret2=passw
    secret=um().match_pass(name, passw)
    if(secret==None):
        secret2=''
        return redirect(url_for('index'))
    else:
        return redirect('/{secret}/mainpage')
    
@app.route('/{secret}/mainpage', methods=['GET','POST'])
def mainpage(name):
    if(secret==name):

        return render_template('mainpage.html',name)
    else:
        return redirect(url_for('index'))
    
@app.route('/{secret}/mainpage/logout', methods=['GET','POST'])
def logout(name):
    if(name==secret):
        secret=''
        secret2=''
        return redirect(url_for('index'))
    
    else:
        if(secret==''):
            return redirect(url_for('index'))
    secret=''
    secret2=''
    return redirect(url_for('index'))

@app.route('/{secret}/mainpage/pass', methods=['GET','POST'])
def changepass(name):
    if(name==secret):
        return render_template('passconfirm.html',name=secret)
    else:
        return redirect(url_for('index'))

@app.route('/{secret}/mainpage/pass/confirm', methods=['GET','POST'])
def changepassconfirm(name):
    if(name!=secret):
        redirect(url_for('index'))
    pass2=request.form['NewPassword']
    if(um().update_pass(secret,secret2,pass2)):
        secret2=pass2
        redirect(url_for('mainpage'),name=secret)

@app.route('/{secret}/mainpage/user' ,methods=['GET','POST'])
def changeuser(name):
    if(name==secret):
        return render_template('userconfirm.html',name=secret)
    else:
        return redirect(url_for('index'))

@app.route('/{secret}/mainpage/user/confirm' ,methods=['GET','POST'])
def changeuserconfirm(name):
    if(name!=secret):
        redirect(url_for('index'))
    pass2=request.form['NewUsername']
    if(um().update_user(secret,pass2,secret2)):
        secret=pass2
        redirect(url_for('mainpage'),name=secret)


app.run(debug=True)





