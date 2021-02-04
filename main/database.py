import sqlite3

conn = sqlite3.connect(r"F:\python project\owlbert-chat\main\db\users.db")



def insert(username, password):
    conn.execute("INSERT INTO users VALUES(\""+ username + "\",\"" + password + "\");")


def read(username):
    ...