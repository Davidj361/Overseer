import pwd

class UserEntry:
    def __init__(self):
        self.loginname = ""
        self.userid = ""
        self.groupid = ""
        self.usercomment = ""
        self.homedir = ""

    def __init__(self, loginname, userid, groupid, usercomment, homedir):
        self.loginname = loginname
        self.userid = userid
        self.groupid = groupid
        self.usercomment = usercomment
        self.homedir = homedir

# We'll have our user list construct itself upon each initialization
class UserList:
    def __init__(self):
        self.userList = {}

        passwdList = pwd.getpwall()
        for passwdEntry in passwdList:
            userEntry = UserEntry(passwdEntry.pw_name, passwdEntry.pw_uid, passwdEntry.pw_gid, passwdEntry.pw_gecos, passwdEntry.pw_dir)
            self.userList[userEntry.userid] = userEntry

    def getLoginname(self, userid):
        userEntry = self.userList.get(userid)
        if userEntry is None:
            return "Error"
        else:
            return self.userList[userid].loginname
