import sqlite3
from twisted.enterprise import util as dbutil

from db_agent import DBAgent

class ServerDBAgent(DBAgent):
    def __init__(self, filename, init_cmds):
        super(ServerDBAgent,self).__init__(filename, init_cmds)

    def fetch_password(self,credentials,callback):
        query = "select rowid,password from users where username = %s" % (
                dbutil.quote(credentials.username, "char"))
        return self._db_conn.runQuery(query).addCallback(
                callback, credentials)
    def fetch_avatar(self,avatar_id,callback):
        query = "select username,fullname from users where rowid = %s" % (
                dbutil.quote(avatar_id, "int"))
        return self._db_conn.runQuery(query).addCallback(callback)
