import sqlite3

def connect():
    con = sqlite3.connect("users.db")
    return con

def close(con):
    con.close()

def create_table():
    con = connect()
    con.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY NOT NULL,
                 password TEXT NOT NULL,
                 email TEXT NOT NULL);''')
    con.close()

def clear_database():
    con = connect()
    con.execute("DROP TABLE IF EXISTS users;")
    con.close()

def create_user(username, password, email):
    con = connect()
    params = (username, password, email)
    con.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?);", params)
    con.commit()
    con.close()

def delete_user(username):
    con = connect()
    params = (username,)
    con.execute("DELETE FROM users WHERE username=?", params)
    con.commit()
    con.close()

def update_user(username, password, email):
    con = connect()
    params = (password, email, username)
    con.execute("UPDATE users SET password=?, email=? WHERE username=?;", params)
    con.commit()
    con.close()

def get_user(username):
    con = connect()
    params = (username,)
    cursor = con.execute("SELECT * FROM users WHERE username=?;", params)
    user = cursor.fetchone()
    con.close()
    return user

def get_username(username):
    con = connect()
    params = (username,)
    cursor = con.execute("SELECT username FROM users WHERE username=?;", params)
    user = cursor.fetchone()
    con.close()
    return user

def get_email(email): 
    con = connect()
    params = (email,)
    cursor = con.execute("SELECT email FROM users WHERE email=?;", params)
    email = cursor.fetchone()
    con.close()
    return email

def get_password(username):
    con = connect()
    params = (username,)
    cursor = con.execute("SELECT password FROM users WHERE username=?;", params)
    password = cursor.fetchone()
    con.close()
    return password