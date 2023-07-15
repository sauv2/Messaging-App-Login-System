from flask import render_template,request,redirect,url_for,abort,session
from message_app_flask.db_urlmatch import username_match as um
from message_app_flask.db_messages import message as m
from message_app_flask.db_sent import sentmessages as sm
from message_app_flask import app
from datetime import datetime, timedelta
import time
from functools import wraps

app.config['SECRET_KEY']='tamilled'


def token_required(f):
    @wraps(f)
    def before_func(*args,**kwargs):
        
        verify=kwargs.get('user')
        if 'user' not in session or session['user']!=verify:
            print(verify)
            print(session)
            abort(401)
        
        return f(*args,**kwargs)
    
    return before_func

def sessionset(user):
    session['user']=user
    print(session['user'])
    return True

def sessionlogout():
    session.pop('user',None)
    return True
 
        

messagepopallowed=['','Username/Password too long or short!','Incorrect Username/Password or User Does not exist!',
                   'Either User Does Not Exist or Has Deleted Their Account','Password Not Correct!','Success! Head Over to Login',
                   'Username/Pass too Long or it Already Exists!'
                ]

@app.route('/')
def welcome():
    if 'user' in session:
        return redirect(url_for('mainpage', user=session['user']))
    return render_template('welcome.html')#1


@app.route('/login')
def login():
    if 'user' in session:
        return redirect(url_for('mainpage', user=session['user']))
    messagepop=request.args.get('messagepop','')
    return render_template('index.html',messagepop=messagepop)#2


@app.route('/mainpage/<user>', methods=['GET', 'POST'])
@token_required
def mainpage(user):
    #links=sm().get_table(user)
    messagepop=request.args.get('messagepop','')
    chatsurl=sm().get_table(user)
    newchatsurl=[]
    for chat in chatsurl:
        newchatsurl.append(chat.split('_')[0])
    return render_template('mainpage.html',user=user,messagepop=messagepop,urls=newchatsurl)#3

@app.route('/between', methods=['GET', 'POST'])
def between():
    try:
        user=request.form['username']
        passw=request.form['password']
        if(len(user)>20 or len(passw)>20 or len(user)==0 or len(passw)==0):
            return redirect(url_for('login', messagepop='Username/Password too long or short!'))
        ans=um().match_pass(user,passw)
        if(ans):
            

            sessionset(user)
            return redirect(url_for('mainpage', user=user,messagepop=''))#3
        else:
            return redirect(url_for('login',messagepop='Incorrect Username/Password or User Does not exist!'))
    except KeyError:
        abort(403)


@app.route('/mainpage/<user>/logout')
@token_required
def logout(user):
    
    tokens=''
    sessionlogout()
    return redirect(url_for('welcome'))

@app.route('/mainpage/<user>/search', methods=['GET', 'POST'])
@token_required
def search(user):
    try:
        srch=request.form['SEARCH']
        ans=um().search(srch)
        if ans ==False:
            return redirect(url_for('mainpage',user=user, messagepop='Either User Does Not Exist or Has Deleted Their Account'))#3
        else:
            return redirect(url_for('message', user=user, receiver=srch))
    except KeyError:
        abort(403)

@app.route('/mainpage/<user>/message/<receiver>')
@token_required
def message(user,receiver):
    
    ans=um().search(receiver)
    if ans is False:
        abort(404)
    sm().create_new(user,receiver)
    sm().create_new(receiver,user)
    messages=m().getmessages(user,receiver)
    open('write.txt', 'w').close()
    file1=open('write.txt','a')
    if(len(messages)==0):
        return render_template('message.html', messagepop='',user=user,receiver=receiver)
    for message in messages:
        
        if(message[0]==0):
            file1.write(f"{user}:{message[1].split('_')[0]} \n")
        else:
            file1.write(f"{receiver}:{message[1].split('_')[0]} \n")
    file1.close()
    file1=open('write.txt','r')
    return render_template('message.html', messagepop=file1.read(),user=user,receiver=receiver)#4

@app.route('/between2/<user>/<receiver>',methods=['GET','POST'])
@token_required
def sendmessage(user,receiver):
    try:
        message=request.form['MESSAGE']
        m().sendmessage(user,receiver,message)
        
        return redirect(url_for('message',user=user,receiver=receiver))
    except KeyError:
        abort(403)

@app.route('/mainpage/<user>/delete')
@token_required
def delete(user):
    return render_template('delete.html', user=user)#5

@app.route('/between3/<user>', methods=['POST'])

def delete_permanent(user):
    try:
        pswd=request.form['pass']
        if(um().match_pass(user,pswd)):
            um().delete_user(user,pswd)
            sessionlogout
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('mainpage',user=user,messagepop='Password Not Correct!'))
    except KeyError:
        abort(404)


@app.route('/register')
def register():
    messagepop=request.args.get('messagepop','')
    return render_template('register.html',messagepop=messagepop)

@app.route('/between4', methods=['GET','POST'])
def register_final():
    try:
        name=request.form['username']
        passw=request.form['password']
        if um().search(name)==True:
            return redirect(url_for('register',messagepop='Username already exists!'))
        if len(name)>20 or len(passw)>20 :
            return redirect(url_for('register',messagepop='Username/Pass too Long'))
        else:
            um().create_user(name,passw)
            return redirect(url_for('register',messagepop='Success! Head Over to Login'))
    except KeyError:
        abort(403)

@app.route('/mainpage/<user>/changepass')
@token_required
def changepassw(user):
    print(user)
    return render_template('changepass.html', user=user)

@app.route('/between5/<user>', methods=['GET','POST'])
def changepass_final(user):
    try:
        oldpass=request.form['current']
        newpass=request.form['new']
        ans=um().update_pass(user,oldpass,newpass)
        if(ans):
            return redirect(url_for('mainpage', user=user, messagepop='Password Updated!'))
        else:
            return redirect(url_for('mainpage', user=user, messagepop='Password Incorrect!'))
    except KeyError:
        abort(403)
    
        