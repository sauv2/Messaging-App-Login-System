import pyodbc

class username_match:
    def __init__(self):
        self.conn=conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=server;DATABASE=username')
        self.cursor=self.conn.cursor()

    def match_pass(self, usr , pswrd):
        query=f"SELECT pswd FROM urlmatch WHERE username= '{usr}';"
        self.cursor.execute(query)
        for pswd in self.cursor.fetchall().first():
            if(pswrd==pswd):
                
                
                return usr
            else:
                return None
        
    
    def create_user(self,usr,pswrd):
        query=f"SELECT pswd FROM urlmatch WHERE username= '{usr}';"
        self.cursor.execute(query)
        for pswd in self.cursor.fetchall():
            if(pswd==None):
               query=f"INSERT INTO urlmatch (loggedin,username,pswd) values (0,'{usr}','{pswrd}');"
               self.cursor.execute(query)
               return True
        return False
    
    def delete_user(self,usr,pswrd):
        query=f"SELECT pswd FROM urlmatch WHERE username= '{usr}';"
        self.cursor.execute(query)
        for pswd in self.cursor.fetchall():
            if(pswrd==pswd):
                query=f"DELETE FROM urlmatch WHERE username= '{usr}';"
                self.cursor.execute(query)
                return True
        return False
    
    def update_user(self,usr,nusr,pswrd):
        query=f"SELECT pswd FROM urlmatch WHERE username= '{nusr}';"
        self.cursor.execute(query)
        for pswd in self.cursor.fetchall():
            if(pswd==None):
                query=f"DELETE FROM urlmatch WHERE username= '{usr}';"
                self.cursor.execute(query)
                query=f"INSERT INTO urlmatch (loggedin,username,pswd) values (0,'{nusr}','{pswrd}');"
                return True
        return False
    
    def update_pass(self,usr,pswrd,npswrd):
        query=f"SELECT pswd FROM urlmatch WHERE username= '{usr}';"
        self.cursor.execute(query)
        for pswd in self.cursor.fetchall():
            if(pswd==pswrd):
                if(npswrd==pswrd):
                    return False
                else:
                    query=f"UPDATE urlmatch SET pswd='{npswrd}' WHERE username='{usr}';"
                    return True
        return False
    
print(username_match().match_pass('admin','123'))

    

            




