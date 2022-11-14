from sqlite3 import Connection
from os import path

class createDatabase:

    def __init__(self, connection):
        self.connection = connection
        if path.exists("database_actions/goodchain.db"):
            self.create_user_table()


    def create_user_table(self):
        self.connection.execute((
            'CREATE TABLE if not exists users('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'username VARCHAR NOT NULL,'
            'password VARCHAR NOT NULL,'
            'coins INTEGER'
            ')'
        ))
        self.connection.commit()




# result = cur.execute('SELECT  name FROM  sqlite_master')
# print(result.fetchone())

# cur.execute("""
#     INSERT INTO users VALUES
#         ('darren', 'test','admin')
# """)
# con.commit()

# result = cur.execute('SELECT * FROM users')
# print(result.fetchall())
