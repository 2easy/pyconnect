from twisted.cred import portal, checkers, credentials, error as credError
from twisted.internet import defer
from zope.interface import Interface, implements

class DBPasswordChecker(object):
    implements(checkers.ICredentialsChecker)
    credentialInterfaces = (credentials.IUsernamePassword,
                            credentials.IUsernameHashedPassword)

    def __init__(self, db_agent):
        self.db_agent = db_agent
    def requestAvatarId(self,credentials):
        pass_ac = self.db_agent.fetch_password(credentials)
        pass_ac.addCallback(self._got_query_results,credentials)
        return pass_ac
    def _got_query_results(self, rows, usr_creds):
        if rows:
            usr_id, password = rows[0]
            return defer.maybeDeferred(
                    usr_creds.checkPassword, password).addCallback(
                        self._checked_password, usr_id)
        else:
            raise credError.UnauthorizedLogin, "No such user"
    def _checked_password(self, matched, usr_id):
        if matched: return usr_id
        else: raise credError.UnauthorizedLogin, "Wrong Password"

class INamedUserAvatar(Interface):
    "should have attributes username and fullname"
class NamedUserAvatar():
    implements(INamedUserAvatar)
    def __init__(self, username, fullname):
        self.username = username
        self.fullname = fullname

class DBRealm():
    implements(portal.IRealm)
    def __init__(self, db_agent):
        self.db_agent = db_agent

    def requestAvatar(self, avatar_id, mind, *interfaces):
        if INamedUserAvatar in interfaces:
            d = self.db_agent.fetch_avatar(avatar_id)
            return d.addCallback(self._got_query_results)
        else:
            raise KeyError("None of the requested interfaces is supported")
    def _got_query_results(self, rows):
        username, fullname = rows[0]
        return (INamedUserAvatar,NamedUserAvatar(username,fullname),
                lambda: None)
