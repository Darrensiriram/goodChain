from sqlite3 import Connection


class login:
    con = Connection

    def __init__(self, username, password):
        self.username = username
        self.password = password
    #TODO: check if credentials match in the system if so send him to the next inlog page
    def loginUser(self):
      print(self.username , self.password)