import sqlite3
from db_agent import DBAgent

class ServerDBAgent(DBAgent):
    def __init__(self, filename, init_cmds):
        super(ServerDBAgent,self).__init__(filename, init_cmds)

    def save_user(self,password):
        try:
            self.c.execute('insert into users values (?)', (password,))
            self.usr_db.commit()
            return self.c.lastrowid
        except:
            return -1

    def fetch_password(self,uid):
        try:
            self.c.execute('select pass from users where rowid = (?)', (uid,))
            (saved_pass,) = self.c.fetchone()
            return saved_pass
        except:
            return ''
