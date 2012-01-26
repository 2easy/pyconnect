import sqlite3
from twisted.enterprise import util as dbutil

from db_agent import DBAgent

class ServerDBAgent(DBAgent):
    def __init__(self, filename, init_cmds):
        super(ServerDBAgent,self).__init__(filename, init_cmds)

    def fetch_password(self, credentials):
        query = "select rowid,password from users where username = %s" %\
                (dbutil.quote(credentials.username, "char"))
        return self._db_conn.runQuery(query)
    def fetch_avatar(self, avatar_id):
        query = "select username,fullname from users where rowid = %s" %\
                (dbutil.quote(avatar_id, "int"))
        return self._db_conn.runQuery(query)
    def find_user(self, username):
        query = "select * from users where username = %s" %\
                (dbutil.quote(username, "text"))
        return self._db_conn.runQuery(query)
    def save_user(self, username, password, fullname):
        query = "insert into users values (%s,%s,%s)" %\
                ( dbutil.quote(username, "text"),
                  dbutil.quote(fullname, "text"),
                  dbutil.quote(password, "text") )
        return self._db_conn.runOperation(query)
