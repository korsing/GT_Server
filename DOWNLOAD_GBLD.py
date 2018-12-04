import MySQLdb
import xlsxwriter

def connectDB():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="4swedu@skku", db="GBLD",charset="utf8mb4")
    c = conn.cursor()
    return c, conn

def writeExcel(file, row, col, content):
    file.write(row, col, content)

c, conn = connectDB()

workbook = xlsxwriter.Workbook("GBLD_DOWNLOAD.xlsx")
USERS = workbook.add_worksheet()
intro = workbook.add_worksheet()
thinking = workbook.add_worksheet()
language = workbook.add_worksheet()

label = [USERS, intro, thinking, language]
category = ["USERS","intro", "thinking", "language"]

for i in range(len(category)):
    row = 0
    query = "SELECT * FROM " + str(category[i]) + " ;"
    c.execute(query)
    data = c.fetchall()
    for tuples in data:
        col = 0
        row += 1
        for element in tuples:
            writeExcel(label[i], row, col, str(element))
            col += 1
            
workbook.close()
