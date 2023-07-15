import pyodbc
from message_app_flask.db_sent import sentmessages


class message:
    def __init__(self):
        self.conn=conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=LAPTOP-HF8AODC3;DATABASE=messages')
        self.cursor=self.conn.cursor()

    def createuser(self,user):
        query1=f"CREATE TABLE {user}_(sent int, username VARCHAR(21) NOT NULL , message NVARCHAR(MAX) NOT NULL, receiver VARCHAR(21) NOT NULL,);"
        print(query1)
        self.cursor.execute(query1)
        self.cursor.commit()

    def deleteuser(self,user):
        query1=f"DROP TABLE {user}_;"
        self.cursor.execute(query1)
        self.cursor.commit()
    
    def getmessages(self,user,receiver):
        
        query1=f"SELECT sent,message FROM {user}_ WHERE receiver = '{receiver}_'"
        self.cursor.execute(query1)
        ans=self.cursor.fetchall()
        messages=[]
        if(len(ans)==0):
            return messages
        for row in ans:
            sub=[]
            sub.append(row[0])
            sub.append(row[1])
            messages.append(sub)
        
        return messages
    
    def sendmessage(self,user,receiver,message):
        query1=f"INSERT INTO {user}_ (sent,message,username,receiver) VALUES ('{0}','{message}_','{user}_','{receiver}_')"
        query2=f"INSERT INTO {receiver}_ (sent,message,username,receiver) VALUES ('{1}','{message}_','{receiver}_','{user}_')"
        self.cursor.execute(query1)
        self.cursor.commit()
        self.cursor.execute(query2)
        self.cursor.commit()
        sentmessages().create_new(user,receiver)
