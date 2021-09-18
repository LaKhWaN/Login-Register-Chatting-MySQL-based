# This file is made by - LaKhWaN

"PROBLEM: --->>> stop using file sys LOL... do it dynamic!"
"""Remote Host
freedb.tech

Database Name
freedbtech_pythonOP

Database Username
freedbtech_pythonop

Database Password
upender9

Email
princelakhwan41@gmail.com

Username
LaKhWaN09"""

from django.http import HttpResponse
from django.shortcuts import render

from . import hashsys
import mysql.connector as sql
import time
import random

# HOST = "freedb.tech"
# USER = "freedbtech_pythonop"
# PASS = "upender9"
# DB = "freedbtech_pythonOP"
HOST = "localhost"
USER = "root"
PASS = ""
DB = "mysql"

mydb = sql.connect(host=HOST,user=USER,passwd=PASS,database=DB)
mycursor = mydb.cursor()

def index(request):
    return render(request,'index.html')
def login(request):
    return render(request,'login.html')

def loginfunc(username,password):
    mycursor.execute("Select username from users")
    users = mycursor.fetchall()
    all_users = ""
    for i in range(len(users)):
        all_users += (users[i][0] + "\n")
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
    if unhashed_password == password:
        print("Logged In")
        return "loggedIn"
    else:
        print("Wrong Password")
        return "wrongPasswd"

def registerfunc(username,password):
    hashedpassword = hashsys.hashing(password)

    # MySQL queries:

    user_tuple = [(username, hashedpassword)]
    sql_query = "Insert into users values(%s,%s)"
    mycursor.executemany(sql_query, user_tuple)
    mydb.commit()
    time.sleep(1)
    print('Registered')
    return "done"

def check(username):
    mycursor.execute("Select username from users")
    users = mycursor.fetchall()
    length = len(users)
    for i in range(length):
        if users[i][0] in username:
            return "taken"

def loginCheck(request):
    username = request.GET.get('username','default')
    password = request.GET.get('password','default')
    print("Username: ",username,"Password: ",password)
    f = open("__cache__.txt",'w')
    f.write(username)
    f.close()
    check = loginfunc(username,password)
    print(check)
    if check == "notFound":
        return HttpResponse("Username not Found")
    elif check == "loggedIn":
        return render(request,'home.html')
    elif check == "wrongPasswd":
        return HttpResponse("Wrong password")

def register(request):
    return render(request,'register.html')

def registerCheck(request):
    username = request.GET.get('username','default')
    password = request.GET.get('password', 'default')
    if len(username) < 6:
        return HttpResponse("Username length doesn't meet the requirment.")
    if len(password) < 6:
        return HttpResponse("Password length doesn't meet the requirment.")
        
    print('username: ',username,"password: ",password)

    checkk = check(username)

    if checkk == "taken":
        return render(request,'usernameTaken.html')
    checkk = registerfunc(username,password)

    if checkk == "done":
        return HttpResponse("Registered!")

def searchfriend(request):
    return render(request,'searchfriend.html')

def makefriend(request):
    fname = request.GET.get("fname")
    try: # Checking if the user is already a friend or not.
        f = open('__cache__.txt','r')
        username = f.read()
        f.close()
        username+="Friend"
        query = f"SELECT friends FROM {username} WHERE friends = '{fname}'"
        mycursor.execute(query)
        data = mycursor.fetchall()
        data = data[0][0]
        if fname == data:
            return HttpResponse("Friend is already in your friendlist")
    except Exception as e: # Continue the code.
        print(e) 
        pass
    query = f"SELECT username FROM users WHERE username='{fname}'"
    mycursor.execute(query)
    found = mycursor.fetchall()
    try: # Searching of user if he is registered or not.
        found = found[0][0]
        f = open('__cache__.txt','r')
        username = f.read()
        f.close()
        username+='Friend'
        query = f"CREATE TABLE IF NOT EXISTS {username}(friends varchar(128))"
        mycursor.execute(query)
        query = f"INSERT INTO {username} VALUES('{found}')"
        mycursor.execute(query)
        mydb.commit()
        return HttpResponse("Friend Added successfully: "+found)
    except Exception as e: # If no user found.
        print("EXCEPTION: ",e)
        return HttpResponse("No User found.\nDid you wrote the username right?")

def searchfriendchat(request):
    return render(request,'searchfriendchat.html')

def livechat(request):
    fname = request.GET.get('fname')
    f = open('__cache__.txt','r')
    username = f.read()
    f.close()
    tablename = username+"Friend"
    query = f"SELECT friends FROM {tablename} WHERE friends = '{fname}'"
    mycursor.execute(query)
    data = mycursor.fetchall()
    if data == []:
        return HttpResponse("No friend found. Please add him in your friendlist.")
    f=open('friendName.txt','w')
    f.write(fname)
    f.close()
    if username>fname:
        tablename = fname+username+'Chat'
    else:
        tablename = username+fname+'Chat'
    query = f"CREATE TABLE IF NOT EXISTS {tablename}(name varchar(128), msg varchar(256))"
    mycursor.execute(query)
    query = f"SELECT msg FROM {tablename} WHERE name = '{fname}'"
    mycursor.execute(query)
    data = mycursor.fetchall()
    length = len(data) - 1
    print("DATA: ",data)
    if data == []:
        lastmessage = "No new message!"
    else:
        lastmessage = data[length][0]
    params = {'fname':fname,'lastmessage':lastmessage}
    return render(request,'livechat.html',params)

def msgsent(request):
    msg = request.GET.get('msg')
    f = open('__cache__.txt','r')
    username = f.read()
    f.close()
    f = open('friendName.txt','r')
    fname  = f.read()
    f.close()
    if username>fname:
        tablename = fname+username+'Chat'
    else:
        tablename = username+fname+'Chat'
    if msg!= "":
        query = f"INSERT INTO {tablename} VALUES('{username}','{msg}')"
        mycursor.execute(query)
        mydb.commit()
    query = f"SELECT msg FROM {tablename} WHERE name = '{fname}'"
    mycursor.execute(query)
    data = mycursor.fetchall()
    length = len(data) - 1
    print("DATA: ",data)
    if data == []:
        lastmessage = "No new message!"
    else:
        lastmessage = data[length][0]
    params = {'fname':fname,'lastmessage':lastmessage}
    return render(request,'livechat.html',params)

def friendlist(request):
    f = open('__cache__.txt','r')
    username = f.read()
    f.close()
    tablename = username+"Friend"
    query = f"SELECT * FROM {tablename}"
    mycursor.execute(query)
    friends = mycursor.fetchall()
    Friends = ""
    for friend in friends:
        Friends+=friend[0]
        Friends+="\n"
    params = {'friends':Friends}
    return render(request,'friendlist.html',params)

def aboutUs(request):
    return render(request,'about-us.html')