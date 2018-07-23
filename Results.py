import MySQLdb
def connectDB():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="4swedu@skku", db="GT_DB",charset="utf8mb4")
    c = conn.cursor()
    return c, conn

c, conn = connectDB()
f=open("results.txt", "w")

c.execute("SELECT * FROM intro")
intro = c.fetchall()

f.write("Start of Intro Survey")
for tuple in intro:
    data = ""
    for column in tuple:
        data += str(column)
    f.write(data)

f.write("-------------------------------------------")

c.execute("SELECT * FROM thinking")
thinking = c.fetchall()

f.write("Start of Thinking Questions")
for tuple in thinking:
    data = ""
    for column in tuple:
        data += str(column)
    f.write(data)

f.write("-------------------------------------------")

c.execute("SELECT * FROM entry")
entry = c.fetchall()

f.write("Start of Entry Questions")
for tuple in entry:
    data = ""
    for column in tuple:
        data += str(column)
    f.write(data)
    
f.write("-------------------------------------------")

c.execute("SELECT * FROM python")
python = c.fetchall()

f.write("Start of Python Questions")
for tuple in python:
    data = ""
    for column in tuple:
        data += str(column)
    f.write(data)

f.write("-------------------------------------------")

c.execute("SELECT * FROM c")
clang = c.fetchall()

f.write("Start of C Questions")
for tuple in clang:
    data = ""
    for column in tuple:
        data += str(column)
    f.write(data)

f.write("-------------------------------------------")

f.close()
