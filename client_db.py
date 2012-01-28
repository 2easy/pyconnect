import sqlite3
from db_agent import DBAgent

class ClientDBAgent(DBAgent):
    def __init__(self,filename, init_cmds):
        super(ClientDBAgent, self).__init__(filename,init_cmds)

    def fetch_all(self):
        try:
            self.c.execute('select * from users')
            return self.c.fetchall()
        except: return []
    def save_user(self, alias, uid, password):
        try:
            self.c.execute('insert into Users values (?,?,?)',
                           (alias, uid, password))
            self.usr_db.commit()
            return True
        except sqlite.OperationalError: return False
