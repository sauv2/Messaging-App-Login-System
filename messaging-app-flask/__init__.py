from flask import Flask,abort,session
import datetime
from functools import wraps


app=Flask(__name__)
st='tamilled'
app.config['SECRET_KEY']='tamilled'
app.permanent_session_lifetime=datetime.timedelta(minutes=60)

def token_required(f):
    @wraps(f)
    def before_func(*args,**kwargs):
        print("hi")
        user=kwargs.get('user')
        if user not in session:
            print("no")
            abort(401)
        print("no1")
        return f(*args,**kwargs)
    print("no2")
    return before_func

def sessionset(user):
    session['user']=user
    print(session['user'])
    return True

def sessionlogout():
    session.pop('user',None)
    return True
 
from message_app_flask import routes

