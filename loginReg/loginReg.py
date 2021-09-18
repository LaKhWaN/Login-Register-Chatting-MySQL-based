# SQL based Login/Register System:

from . import hashsys
import mysql.connector
import time
import random

# Register:

mydb = mysql.connector.connect(host='localhost',user='root',passwd='',database='python')
mycursor = mydb.cursor()

# Random number for hashtag.
def check(username):
    mycursor.execute("Select username from users")
    users = mycursor.fetchall()
    length = len(users)
    for i in range(length):
        if users[i][0] in username:
            return "taken"
            
def register(username,password):
    hashedpassword = hashsys.hashing(password)

    # MySQL queries:

    user_tuple = [(username, hashedpassword)]
    sql_query="Insert into users values(%s,%s)"
    mycursor.executemany(sql_query,user_tuple)
    mydb.commit()
    time.sleep(1)
    print('Registered')
    return "done"

# Login

def loginfunc(username,password):
    mycursor.execute("Select username from users")
    users = mycursor.fetchall()
    all_users = ""
    for i in range(len(users)):
        all_users+= (users[i][0]+"\n")
    if username not in all_users:
        print("Username not found.")
        return "notFound"
    
    sql_query = ("SELECT username from users")
    unhashed_password = mycursor.execute(sql_query)
    users = mycursor.fetchall()
    for user_tuple in users:
        for user in user_tuple:
            if user == username:
                sql_query2 = ("SELECT password from users where username ='{}'".format(username))
                mycursor.execute(sql_query2)
                sql_password = mycursor.fetchall()
                for passwd in sql_password:
                    for sql_passwd in passwd:
                        real_password = sql_passwd
                        unhashed_password = hashsys.unhash(real_password)
    if  unhashed_password == password:
        print("Logged In")
        return "loggedIn"
    else:
        print("Wrong Password")
        return "wrongPasswd"
