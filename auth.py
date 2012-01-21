from twisted.cred import portal, checkers, credentials, error as credError
from twisted.internet import defer
from zope.interface import Interface, implements

class PasswordDictChecker(object):
    implements(checkers.ICredentialsChecker)
    credentialInterfaces = (credentials.IUsernamePassword,)

    def __init__(self, passwords):
        self.passwords = passwords
    def requestAvatarId(self,credentials):
        username = credentials.username
        if self.passwords.has_key(username):
            if credentials.password == self.passwords[username]:
                return defer.succeed(username)
            else:
                return defer.fail(credError.UnauthorizedLogin("Wrong password"))
        else:
            return defer.fail(credError.UnauthorizedLogin("No such user"))

class INamedUserAvatar(Interface):
    "should have attributes username and fullname"
class NamedUserAvatar():
    implements(INamedUserAvatar)
    def __init__(self, usr_id, fullname):
        self.usr_id = usr_id
        self.fullname = fullname

class UserAvatarsRealm():
    implements(portal.IRealm)
    def __init__(self, users):
        self.users = users

    def requestAvatar(self, avatarId, mind, *interfaces):
        if INamedUserAvatar in interfaces:
            fullname = self.users[avatarId]
            logout = lambda: None
            return (INamedUserAvatar,NamedUserAvatar(avatarId, fullname),logout)
        else:
            raise KeyError("None of the requested interfaces is supported")
