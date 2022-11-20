from sqlite3 import Connection
from os import path


class createDatabase:

    def __init__(self, connection):
        self.connection = connection
        if path.exists("database_actions/goodchain.db"):
            self.create_user_table()
            self.create_connectivity_table()

    def create_user_table(self):
        self.connection.execute((
            'CREATE TABLE if not exists users('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'username VARCHAR NOT NULL,'
            'password VARCHAR NOT NULL,'
            'coins INTEGER,'
            'private_key VARCHAR,'
            'public_key VARCHAR'
            ')'
        ))
        self.connection.commit()

    def create_connectivity_table(self):
        self.connection.execute((
            'CREATE TABLE if not exists connectivity('
            'id INTEGER PRIMARY KEY,'
            'connection_count INTEGER NOT NULL,'
            'currentTime TIMESTAMP'
            ')'
        ))
        self.connection.commit()

    def first_connection(self):
        self.connection.execute('INSERT INTO connectivity (connection_count) VALUES (1)')
        self.connection.commit()
