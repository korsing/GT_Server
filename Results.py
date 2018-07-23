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
worksheet = workbook.add_worksheet()

# 가로 타이틀 작성
writeExcel(worksheet, 0,0, "Seq")
writeExcel(worksheet, 0,1, "UserID")

for i in range(2, 28):
    writeExcel(worksheet, i,0, i-2)

category = ["intro", "thinking", "entry", "python", "c"]

row = 1
for i in range(len(category)):
    col = 1
    c.execute("SELECT * FROM %s",(category[i],))
    data = c.fetchall() # DB 안에 있는 내용을 튜플로 가져옴
    for tuples in data:
        for element in tuples:
            writeExcel(worksheet, row, col, str(element))
            col += 1
        row += 1


