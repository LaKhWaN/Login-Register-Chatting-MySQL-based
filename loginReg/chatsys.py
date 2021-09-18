import mysql.connector as sql

HOST = "localhost"
USER = "root"
PASS = ""
DB = "python"
mydb = sql.connect(host=HOST,user=USER,passwd=PASS,database=DB)

mycursor = mydb.cursor()
  
def listen(FriendName):
    mycursor.execute(f"SELECT message FROM chatsys WHERE NAME='{FriendName}'")
    data=mycursor.fetchall()
    length=len(data) - 1
    return data[length][0]

def commit(Name,Msg):
    query = f"INSERT INTO chatsys VALUES('{Name}','{Msg}')"
    mycursor.execute(query)
    mydb.commit()