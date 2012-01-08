import sqlite3

class DBAgent(object):
    def __init__(self,filename,init_cmds):
        import os
        if not os.path.exists(filename):
            self.usr_db = sqlite3.connect(filename)
            self.c = self.usr_db.cursor()
            try:
                for cmd in init_cmds:
                    self.c.execute(cmd)#'create Table Users (User_id int, Pass text)')
            except sqlite3.DatabaseError, msg:
                print msg
            self.usr_db.commit()
        else:
            self.usr_db = sqlite3.connect(filename)
            self.c = self.usr_db.cursor()

