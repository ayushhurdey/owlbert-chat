import sqlite3

#F:\python project\owlbert-chat\main\db\users.db
url = r"F:\project\python projects\owlbert-chat\main\db\users.db"
conn = ""

def openConnection():
    global conn
    conn = sqlite3.connect(url, check_same_thread=False)

def closeConnection():
    global conn
    conn.close()

def getAllUsers():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    return cursor.fetchall()

def getAllChats():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chats;")
    return cursor.fetchall()

def checkUserIfPresent(username):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = \""+ username + "\";")
    if not cursor.fetchall():
        return False
    else:
        return True

def insertUser(username, password):
    try:
        conn.execute("INSERT INTO users VALUES(\""+ username + "\",\"" + password + "\");")
        conn.commit()
    except Exception as e:
        print("Valus not inserted inside users :",  e)
    
    return True


def insertChat(data):
    try:
        conn.execute('''INSERT INTO chats(username,send_msg,response_msg,timestamp) 
                        VALUES("''' + data['username'] + '''",
                        "''' +data['send_msg']+ '''",
                        "''' +data['response_msg']+ '''",
                        "'''+data['timestamp']+'''");''')
        conn.commit()
    except Exception as e:
        print("!! Values not inserted in chats :",e)
    
    return True
    

def validateUser(username, password):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = \""+ username +"\" AND password = \"" + password +"\"")
    if not cursor.fetchall():
        return False
    else:
        return True


def readChatsForUser(username):
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM chats
                      WHERE username="''' + username + '''"
                      GROUP BY timestamp;''')
    chatLists = cursor.fetchall()

    chats = {}
    for each in chatLists:
        chats[each[0]] = {}
    for each in chatLists:
        chats[each[0]]['username'] = each[1]
        chats[each[0]]['send_msg'] = each[2]
        chats[each[0]]['response_msg'] = each[3]
        chats[each[0]]['timestamp'] = each[4]
    return chats    