import MySQLdb
import xlsxwriter

def connectDB():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="4swedu@skku", db="GT_DB",charset="utf8mb4")
    c = conn.cursor()
    return c, conn

def writeExcel(file, row, col, content):
    file.write(row, col, content)

c, conn = connectDB()
# 엑셀파일 생성
workbook = xlsxwriter.Workbook("results.xlsx")
USERS = workbook.add_worksheet("users")
intro = workbook.add_worksheet("intro")
thinking = workbook.add_worksheet("thinking")
clang = workbook.add_worksheet("clang")
python = workbook.add_worksheet("python")
entry = workbook.add_worksheet("entry")
label = [USERS, intro, thinking, clang, python, entry]

workbook = xlsxwriter.Workbook("GT_DOWNLOAD.xlsx")
worksheet = workbook.add_worksheet()


writeExcel(worksheet, 0,0, "Seq")
writeExcel(worksheet, 0,1, "UserID")

for i in range(25):
    writeExcel(worksheet, 0,i+2, i+1)

category = ["USERS","intro", "thinking", "c", "python", "entry"]

row = 1
for i in range(len(category)):
    query = "SELECT * FROM " + str(category[i]) + " ;"
    c.execute(query)
    data = c.fetchall()
    for tuples in data:
        col = 1
        row += 1
        for element in tuples:
            writeExcel(label[i], row, col, str(element))
            col += 1
        

workbook.close()
