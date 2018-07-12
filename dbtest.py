#-*- coding: utf-8-*-
import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="4swedu@skku", db="GT_DB", charset="utf8mb4")
    c = conn.cursor()
    return c, conn

name = "Joshua Jung"
userid = "korsing03330"
userpw = "dbsdud12"
email = "joshuanpedia@gmail.com"
phone = "010-2614-5698"
school = "Do Sung Elementary School"

c, conn = connection()
c.execute('INSERT INTO USERS VALUES (%s, %s, %s, %s, %s, %s)', (name, userid, userpw, email, phone, school))

id = 'korsing'
c.execute("SELECT * FROM USERS WHERE userid = ('%s')", id)
print(c.fetchall()[0])

c.execute("SELECT userpw FROM USERS WHERE userid = 'korsing'")
print(c.fetchone())

conn.commit()
conn.close()
