import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="4swedu@skku", db="GT_DB")
    c = conn.cursor()
    return c, conn

name = "정윤석"
userid = "korsing"
userpw = "dbsdud12"
email = "joshuanpedia@gmail.com"
phone = "010-2614-5698"
school = "도성초등학교"

c, conn = connection()
c.execute("INSERT INTO USERS VALUES (%s, %s, %s, %s, %s, %s)",\
          (name, userid, userpw, email, phone, school))

c.execute("SELECT * FROM USERS")
print(c.fetchall())

conn.commit()
conn.close()
