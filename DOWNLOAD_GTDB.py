import MySQLdb
import xlsxwriter

def connectDB():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="4swedu@skku", db="GT_DB",charset="utf8mb4")
    c = conn.cursor()
    return c, conn

def writeExcel(file, row, col, content):
    file.write(row, col, content)

# DB연결
c, conn = connectDB()
# 엑셀파일 생성
workbook = xlsxwriter.Workbook("results.xlsx")
USERS = workbook.add_worksheet("users")
intro = workbook.add_worksheet("intro")
thinking = workbook.add_worksheet("thinking")
c = workbook.add_worksheet("c")
python = workbook.add_worksheet("python")
entry = workbook.add_worksheet("entry")
label = [USERS, intro, thinking, c, python, entry]
category = ["USERS","intro", "thinking", "c", "python", "entry"]

row = 1
for i in range(len(category)):
    query = "SELECT * FROM " + str(category[i]) + " ;"
    c.execute(query)
    data = c.fetchall() # DB 안에 있는 내용을 튜플로 가져옴
    for tuples in data:
        col = 1
        row += 1
        for element in tuples:
            writeExcel(label[i], row, col, str(element))
            col += 1
        

workbook.close()
