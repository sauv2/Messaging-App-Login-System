import pyodbc

class sentmessages:
    def __init__(self):
        self.conn=conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=LAPTOP-HF8AODC3;DATABASE=sentmessages')
        self.cursor=self.conn.cursor()

    def get_table(self,user):
        query1=f"SELECT receiver FROM {user}_ WHERE username = '{user}_'"
        self.cursor.execute(query1)
        ans=self.cursor.fetchall()
        sent_to=[]
        if(len(ans)==0):
            return sent_to
        else:
            for rec in ans:
                sent_to.append(rec[0])
            return sent_to
    
    def create_table(self,user):
        query1=f"CREATE TABLE {user}_ (username VARCHAR(21), receiver VARCHAR(21) UNIQUE);"
        self.cursor.execute(query1)
        self.cursor.commit()

    def create_new(self,user,receiver):
        query1=f"SELECT * FROM {user}_ WHERE receiver = '{receiver}_'"
        self.cursor.execute(query1)
        ans=self.cursor.fetchall()
        if(len(ans)!=0):
            return 
        else:
            query2=f"INSERT INTO {user}_ (username, receiver) VALUES ('{user}_', '{receiver}_')"
            self.cursor.execute(query2)
            self.cursor.commit()
            return
        
    def delete_table(self,user):
        
        query1=f"DROP TABLE {user}_ "
        self.cursor.execute(query1)
        self.cursor.commit()
    
    

        