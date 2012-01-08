import sqlite3

class DBAgent():
    def __init__(self,filename):
        import os
        if not os.path.exists(filename):
            self.usr_db = sqlite3.connect(filename)
            self.c = self.usr_db.cursor()
            try:
                self.c.execute('create Table Users (User_id int, Pass text)')
            except sqlite3.DatabaseError, msg:
                print msg
            self.usr_db.commit()
        else:
            self.usr_db = sqlite3.connect(filename)
            self.c = self.usr_db.cursor()
    def save_user(self,uid,password):
        try:
            self.c.execute('insert into Users values (?,?)', (uid , password))
            self.usr_db.commit()
        except sqlite.OperationalError, msg: return False
        # if everything went well...
        return True
