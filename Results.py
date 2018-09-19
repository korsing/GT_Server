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
workbook = xlsxwriter.Workbook("DATABASE.xlsx")
worksheet = workbook.add_worksheet()

# 가로 타이틀 작성
writeExcel(worksheet, 0,0, "Seq")
writeExcel(worksheet, 0,1, "UserID")

for i in range(25):
    writeExcel(worksheet, 0,i+2, i+1)

category = ["intro", "thinking", "language"]

row = 1
for i in range(len(category)):
    query = "SELECT * FROM " + str(category[i]) + " ;"
    c.execute(query)
    data = c.fetchall() # DB 안에 있는 내용을 튜플로 가져옴
    for tuples in data:
        col = 1
        row += 1
        for element in tuples:
            writeExcel(worksheet, row, col, str(element))
            col += 1
        

workbook.close()
