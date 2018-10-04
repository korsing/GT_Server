import MySQLdb
import xlsxwriter

def connectDB():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="4swedu@skku", db="GBLD",charset="utf8mb4")
    c = conn.cursor()
    return c, conn

def writeExcel(file, row, col, content):
    file.write(row, col, content)

# DB연결
c, conn = connectDB()
# 엑셀파일 생성
workbook = xlsxwriter.Workbook("results.xlsx")
worksheet = workbook.add_worksheet()
thinking = workbook.add_worksheet()
language = workbook.add_worksheet()

# 가로 타이틀 작성
writeExcel(worksheet, 0,0, "USER ID")
writeExcel(worksheet, 0,1, "Q1")
writeExcel(worksheet, 0,1, "Q2")
writeExcel(worksheet, 0,1, "Q3")
writeExcel(worksheet, 0,1, "Q4")
writeExcel(worksheet, 0,1, "Q5")
writeExcel(worksheet, 0,1, "Q6")
writeExcel(worksheet, 0,1, "Q7")
writeExcel(worksheet, 0,1, "Q8")
writeExcel(worksheet, 0,1, "Q9")
writeExcel(worksheet, 0,1, "Q10")
writeExcel(worksheet, 0,1, "Q11")
writeExcel(worksheet, 0,1, "Q12")
writeExcel(worksheet, 0,1, "Q13")
writeExcel(worksheet, 0,1, "Q14")
writeExcel(worksheet, 0,1, "Q15")

category = ["USERS","intro", "thinking", "language"]

row = 1
for i in range(len(category)):
    query = "SELECT * FROM " + str(category[i]) + " ;"
    c.execute(query)
    data = c.fetchall()
    for tuples in data:
        col = 1
        row += 1
        for element in tuples:
            writeExcel(worksheet, row, col, str(element))
            col += 1
            
workbook.close()
