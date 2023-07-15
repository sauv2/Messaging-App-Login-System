import pyodbc
from message_app_flask.db_messages import message
from message_app_flask.db_sent import sentmessages

class username_match:
    def __init__(self):
        self.conn=conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=LAPTOP-HF8AODC3;DATABASE=usernames')
        self.cursor=self.conn.cursor()

    def search(self,user):
        query=f"SELECT username FROM urlmatch WHERE username='{user}_'"
        self.cursor.execute(query)
        ans=self.cursor.fetchall()
        if(len(ans)==0):
            return False
        return True
        
    def match_pass(self, usr , pswrd):
        query=f"SELECT pswd FROM urlmatch WHERE username= '{usr}_';"
        self.cursor.execute(query)
        ans=self.cursor.fetchall()
        if(len(ans)==0):
            return False
        for pswd in ans:
            if(pswrd + str('_')==pswd[0]):
                return True
            else:
                return False
        
    
    def create_user(self,usr,pswrd):
        query=f"SELECT pswd FROM urlmatch WHERE username= '{usr}_';"
        self.cursor.execute(query)
        ans=self.cursor.fetchall()
        
        if(len(ans)>0):
            print("yes")
            return False    
        query1=f"INSERT INTO urlmatch (loggedin,username,pswd) values (0,'{usr}_','{pswrd}_');"
        print(query1)
        self.cursor.execute(query1)
        self.cursor.commit()
        message().createuser(usr)
        sentmessages().create_table(usr)
        return True
        
    
    def delete_user(self,usr,pswrd):
        query=f"SELECT pswd FROM urlmatch WHERE username= '{usr}_';"
        self.cursor.execute(query)
        ans=self.cursor.fetchall()
        if(len(ans)==0):
            return False
        
        for pswd in ans:
            if(pswrd + str('_')==pswd[0]):
                query1=f"DELETE FROM urlmatch WHERE username= '{usr}_';"
                self.cursor.execute(query1)
                self.cursor.commit()
                message().deleteuser(usr)
                sentmessages().delete_table(usr)
                return True
        return False
    
    
    def update_pass(self,usr,pswrd,npswrd):
        query=f"SELECT pswd FROM urlmatch WHERE username='{usr}_' AND pswd='{pswrd}_' "
        self.cursor.execute(query)
        ans=self.cursor.fetchall()
        if(len(ans)==0):
            return False
        else:
            query1=f"UPDATE urlmatch SET pswd='{npswrd}_' WHERE username='{usr}_';"
            self.cursor.execute(query1)
            self.cursor.commit()
            return True
           
    
    #query1=f"UPDATE urlmatch SET pswd='{npswrd}_' WHERE username='{usr}_';"
    #query=f"SELECT pswd FROM urlmatch WHERE username= '{usr}_';"
    
    


    
