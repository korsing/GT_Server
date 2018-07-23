import MySQLdb
def connectDB():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="4swedu@skku", db="GT_DB",charset="utf8mb4")
    c = conn.cursor()
    return c, conn

def writeIn(filename, mass):
    for tuple in mass:
        for column in tuple:
            filename.write(str(column)+' / ')
            filename.write('\n')
        filename.write('\n')
    filename.write('---------------------------------------\n')

c, conn = connectDB()
f=open("results.txt", "w")

c.execute("SELECT * FROM intro")
intro = c.fetchall()
f.write("Start of Intro Survey! \n")
writeIn(f, intro)

c.execute("SELECT * FROM thinking")
thinking = c.fetchall()
f.write("Start of Thinking Questions! \n")
writeIn(f, thinking)

c.execute("SELECT * FROM entry")
entry = c.fetchall()
f.write("Start of Entry Questions! \n")
writeIn(f, intro)

c.execute("SELECT * FROM python")
python = c.fetchall()
writeIn(f, python)

c.execute("SELECT * FROM c")
clang = c.fetchall()
f.write("Start of C Questions! \n")
writeIn(f, clang)

f.close()
