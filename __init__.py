                    #-*- coding: utf-8-*-
from flask import Flask, render_template, session, redirect, flash, request
from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, SelectField, RadioField
from wtforms.validators import InputRequired, Email, Length
import MySQLdb
import os
from werkzeug.security import generate_password_hash, check_password_hash


# Flask가 동작하기 위해서 필요한 기본 설정 들..
app = Flask(__name__)
app.config['SECRET_KEY'] = "HansClass"
app.secret_key = os.urandom(50)



# 입력 칸을 정의하는 클래스 선언
class LoginForm(Form):
    userid = StringField("username", validators=[InputRequired()])
    userpw = PasswordField("password", validators=[InputRequired()])



# DB 연동을 수행하는 함수
def connectDB():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="4swedu@skku", db="GBLD", charset="utf8mb4")
    c = conn.cursor()
    return c, conn

# 로그인을 수행했을 때 세션을 생성하는 함수
def createSession(userid):
    session['user'] = userid

# 로그아웃 함수
def deleteSession():
    session.pop('user', None)

def createError(message):
    session['errmsg'] = message

def deleteError():
    session.pop('errmsg', None)

# 홈페이지 # 로그인 없이는 각 버튼 접근 권한 없애야함!
@app.route('/')
def homepage():
    if('user' in session):
        userid = session['user']
        c, conn = connectDB()
        c.execute("SELECT name FROM USERS WHERE userid = %s", (userid,))
        name = c.fetchone()[0]
        return render_template("index.html", name=name, userid=userid, flag = True)
    else:
        return render_template("index.html", name="NULL", flag = False)

@app.route('/error')
def error():
    if('user' not in session):
        if('errmsg' in session): # 현재 무슨 에러가 발생했다면
            message = session['errmsg'] # 무슨 에러인지 메세지 갖고오고
        else: # 동작하는지 테스트용도.. 실제로 이 url 치고 들어오는 사람은 없을테니까
            message = ("Congrats! There is no error found.")
        return render_template("/admin/error.html", message = message[:], flag = False) #변수가 안넘어감
    else:
        return render_template("/admin/error.html", message = message[:], flag = True)

@app.route('/deleteerror')
def testtest():
    deleteError()
    return redirect('/error')

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if(login_form.validate_on_submit()): # 로그인 버튼이 눌렸을 때 수행되는 코드
        c, conn = connectDB() # DB에 연결하고
        userid = login_form.userid.data # 입력받은 아이디와
        c.execute("SELECT userpw FROM USERS WHERE userid = %s", (userid,)) # 아이디를 사용하여 비밀번호를 DB에서 가져옴
        userpw_tuple = c.fetchone() 
        c.execute("SELECT phone FROM USERS WHERE userid = %s", (userid,)) # 아이디를 사용하여 비밀번호를 DB에서 가져옴
        userphone_tuple = c.fetchone() # ('010-2614-5698',)
        userphone = userphone_tuple[0][9:13] # 5698 출력 성공

        if(userpw_tuple==None): # 갖고온게 하나도 없다는 말은 userid가 존재하지 않는다!
            message = "Your ID or PASSWORD seems to be wrong!"
            createError(message)
            return redirect('/error')
        else:
            if(check_password_hash(userpw_tuple[0], login_form.userpw.data)): # 입력한 비밀번호와 DB상의 비밀번호가 같다면
                createSession(userid) # 로그인이 완료된 상황이니 세션을 생성
                return redirect('/')
            elif (login_form.userpw.data == userphone): # 비번은 일치하지 않는데 전화번호 뒷 4자리를 입력했다면
                createSession(userid)
                return redirect('/')
            else: # 입력한 비밀번호가 DB와 다르다면
                message = "Your ID or PASSWORD seems to be wrong!"
                createError(message)
                return redirect('/error')
    return render_template("/admin/login.html", form=login_form)

@app.route('/onlyformembers')
def onlyformembers():
    return render_template("/admin/onlyformembers.html", flag = False)

@app.route('/returnuser')
def returnuser():
    if('user' in session):
        userid = session['user']
        c, conn = connectDB()
        c.execute("SELECT lastnumber FROM lastquestion WHERE userid = %s", (userid,))
        qnum = c.fetchone()[0]
        return redirect("/leveltest/Q"+str(qnum))
    else:
        return redirect("/onlyformembers")
    return render_template("/assessments/abouttest.html")

   
@app.route('/findidorpassword')
def findidorpassword():
    return render_template("/admin/findidorpassword.html")

class FindidForm(Form):
    name = StringField("name", validators=[InputRequired()])
    school = StringField("school", validators=[InputRequired()])
    schoolid = StringField("schoolsid", validators=[InputRequired()])

@app.route("/findid", methods=['GET', 'POST'])
def findid():
    findid_form =  FindidForm()
    if(findid_form.validate_on_submit()):
        c, conn = connectDB()
        query = "SELECT userid FROM USERS WHERE school = '" + findid_form.school.data + "' AND studNo = '" + findid_form.schoolid.data + "' AND name = '" + findid_form.name.data + "';" 
        check = c.execute(query)
        check=int(check)
        return "여기까진"
        c.execute("SELECT userid FROM USERS WHERE school = %s and studNo = %s and name = %s", (findid_form.school.data,findid_form.schoolid.data, findid_form.name.data))
  
        userid = c.fetchone()[0]
        conn.commit()
        conn.close()
        
        if(check > 0):
            return render_template("/admin/showid.html",userid = userid)
        else:
            
            message = "You're information is something wrong!!"
            createError(message)
            return redirect('/error')
    return render_template("/admin/findid.html", form = findid_form)

@app.route("/findpassword")
def findpassword():
    return render_template("admin/findpassword.html")
@app.route('/logout')
def logout():
    deleteSession()
    return redirect('/')





# 회원가입란을 정의하는 클래스 선언
class SignupForm(Form):
    userpw = PasswordField("password", validators=[InputRequired()])
    pwconfirm = PasswordField("password", validators=[InputRequired()])
    name = StringField("name", validators=[InputRequired()])
    school = StringField("school", validators=[InputRequired()])
    schoolid = StringField("schoolsid", validators=[InputRequired()])
    phone = StringField("phone", validators=[InputRequired()])


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    if(signup_form.validate_on_submit()):
        if(len(signup_form.userpw.data) < 8): # 비밀번호가 8자리 이상인지 체크
            message = "PASSWORD must be more than 8 characters."
            createError(message)
            return redirect('/error')

        if(signup_form.userpw.data != signup_form.pwconfirm.data): # 비밀번호와 비밀번호 확인이 일치하는지 체크
            message = "PASSWORDs do not match!"
            createError(message)
            return redirect('/error')
        
        # 전화번호 일관성있게 다듬기
        phone = signup_form.phone.data
        if(len(phone)<13):
            message = "Invalid Phone Number.."
            createError(message)
            return redirect('/error')



        c, conn = connectDB()
        
        query = "SELECT userid FROM USERS WHERE school = '" + signup_form.school.data + "' AND studNo = '" + signup_form.schoolid.data + "';" 
        check = c.execute(query) # 이 값은 나온 값의 개수로 정상적으로 나오는데 return은 안됌..
        
        if(check):
            message = "You have already signed up!"
            createError(message)
            return redirect('/error')

        # 아이디 자동 생성
        c.execute("SELECT COUNT(*) FROM USERS;")
        counter = c.fetchone()[0]

        if(counter<10):
            counter='000'+str(counter+1)
        elif(counter<100):
            counter='00'+str(counter+1)
        elif(counter<1000):
            counter='0'+str(counter+1)

        userid = "GBLD" + counter

        # 이까지 온다는 것 자체가 위에 에러 if문에서 하나도 안걸렸다는 말!
        password = generate_password_hash(signup_form.userpw.data)
        c.execute("INSERT INTO USERS VALUES (%s, %s, %s, %s, %s, %s)", (userid, password, signup_form.name.data, signup_form.school.data, signup_form.schoolid.data, phone))
        lists = ["intro", "thinking", "entry", "python", "c", "lastquestion"]
        for category in lists:
            query = "INSERT INTO " + category + "(userid) VALUES ('" + userid +"')"
            c.execute(query)
            if (category == "lastquestion"):
                query = "UPDATE lastquestion set lastnumber  = 1  WHERE userid = '" + userid + "';"
                c.execute(query)

        conn.commit()
        conn.close()

        createSession(userid)
        return render_template("/assessments/questions/intro/StartPage.html")
    return render_template("/admin/signup.html", form = signup_form)

@app.route("/leveltest")
def leveltest():
    if('user' in session):
        return render_template("/assessments/leveltest.html", flag = True)
    else:
        return redirect("/onlyformembers")

@app.route("/endtest")
def endtest():
    if('user' in session):
        
        return render_template("/")
    else:
        return redirect("/onlyformembers")

@app.route("/realend/<var>", methods=['GET', 'POST'])
def realend(var):
    if('user' in session):
        if (var == 'y'):
           deleteSession()
           return redirect("/")
        elif (var == 'n'):
           
           return redirect("/leveltest")
        
    else:
        return redirect("/onlyformembers")

@app.route('/abouttest')
def aboutleveltest():
    if('user' in session):
        userid = session['user']
        c, conn = connectDB()
        c.execute("SELECT name FROM USERS WHERE userid = %s", (userid,))
        name = c.fetchone()[0]
        return render_template("/assessments/abouttest.html", name=name, flag = True)
    else:
        return redirect("/onlyformembers")
    return render_template("/assessments/abouttest.html")



# 초기 설문조사를 위한 클래스 선언
class IntroForm(Form):
    answer = RadioField('Label', choices=[('value', 'description'), ('value_two', 'whatever')])

# 레벨테스트란을 정의하는 클래스 선언
class QuestionForm(Form):
    answer = RadioField('Label', choices=[('value', 'description'), ('value_two', 'whatever')])

def get_CAT(qnum):
    if(qnum <= 10):
        category = "intro"
    elif(qnum <= 30):
        category = "thinking"
    elif(qnum <= 50):
        category = "entry"
    elif(qnum <= 70):
        category = "python"
    elif(qnum <= 90):
        category = "c"
    else:
        message = "Something seems to have gone wrong!"
        createError(message)
        return redirect('/error')

    return category

@app.route("/leveltest/Q<qnum>", methods=['GET', 'POST'])
def questions(qnum):
    if('user' in session):
        category = get_CAT(int(qnum))
        if(category == "intro"):
            bogi = ["Always by myself.", "Depends on who.", "Always with friends."]
        elif(category == "thinking"):
            bogi=[3,4,5,7,10,12,14,15,19,24,30,32,36,39,40,41,43,45,50,62,65,70,80,100,120,150, 180, 210, 300, 320,  'ab','bd','ac','ad','bc','bcad','cadb','dbca','dacb','dabc']
            thinking_Answer=[14,30,3,2,2,10,32,19,6,4,16,11,14,39,21,2,13,9,13,4]
        elif(category == "entry"):
            bogi = [1,2,3,4,5,6,7,8,9,10,11,12,13,20,21,25,31,40,45,50,55,56,60,70,75,80,95,100,120,210,250,251,260,261,262,263,'A','B','C','D']
            Entry_Answer = [27,38,6,32,15,17,30,3,18,16,29,3,20,3,5,19,13,14,1,4]
        elif(category == "python"):
            bogi = [0, 1, 2, 3, 4, 6, 7, 8, 9, 10,"1, 2", "2, 3", 13, 14, 15,"2, 3, 4", "3, 4, 5", "3, 4, 6", "2, 4", "2, 5","L[i] > B", "L[i] < B", "L[i] == B", 300, 400, "True", "False", "10-x", "10-y", "10-z", 79, 80, "X, Y", "Y, Z", "Z, X", "int()", "str()", "type()", "break", "continue"]
            python_Answer = [28, 9, 15, 32, 12, 10, 13, 40, 21, 1, 26, 18, 4, 20, 33, 26, 36, 1, 25, 33]
        else:
            bogi = ["x z y","y z x","x x z","y x z","x y z","x y","y y","x x","y x","x / 2","x % 2","x % 10","x // 10","i > 9","i <= 9","i < 7","i <= 7","5","0","1","100","130","200","400","1 1","2 1","2 2","2 3","3 2","3 3","4 4","6 2","5 10","10 5","10 11","11 10","11 16","12 16","45 10","45 9"] 
            c_answer = [3, 33, 23, 6, 4, 29, 11, 15, 5, 24, 9, 39, 36, 12, 30, 16, 37, 26, 18, 32]
            
        
        return render_template("/assessments/questions/" + category +"/Q" + str(qnum) + ".html", bogi=bogi, qnum=qnum, flag = True)
    else:
        return redirect("/onlyformemebers")

@app.route("/leveltest/<variable>", methods=['GET', 'POST'])
def leveltest_category(variable):
    if(variable[0] != 'Q'):
        if('user' in session):
            userid = session['user']
            c, conn = connectDB()
            query = "SELECT * FROM " + variable + " WHERE userid = '" + userid + "';"
            c.execute(query)

            datalist = c.fetchall()
            passorfail = []
            if(len(datalist) == 0):
                if(variable == 'intro'):
                    length = 7
                else:
                    length = 25
                for i in range(length):
                    passorfail.append('X')

            else:
                for column in datalist[0][1:]:
                    if(column != None):
                        passorfail.append("O")
                    else:
                        passorfail.append("X")

            difficulty = ["BEGINNER", "EASY", "STANDARD", "DIFFICULT", "CHALLENGING"]
            category_list = ['thinking', 'entry', 'python', 'c', 'intro']
            if(variable in category_list):
                return render_template("/assessments/questions/" + variable + "/start.html", PassorFail=passorfail, difficulty = difficulty, flag = True)
        else:
            return redirect("/onlyformembers")

@app.route('/A<qnum>/<answer>')
def addAnswertoDB(qnum, answer):
    if('user' in session):
        userid = session['user']
        category = get_CAT(int(qnum))
# 이까지는 됨
        c, conn = connectDB()
        query = "UPDATE " + category + " SET Q" + qnum + " = " + answer + " WHERE userid = '" + userid + "';"
# 이까지는 됨
        c.execute(query)
        query = "UPDATE lastquestion set lastnumber  = "+ qnum +" WHERE userid = '" + userid + "';"
        c.execute(query)
        conn.commit()
        c.close()

        if (category == "intro"):
            if int(qnum)!= 10:
                url="/leveltest/Q"+str(int(qnum)+1)
            else:
                return render_template("/assessments/questions/intro/GoNextPage.html")
        else:
            url = "/leveltest/" + category
        return redirect(url)
        
    else:
        return redirect("/onlyformembers")


@app.route('/dashboard')
def printdb():
    if('user' in session):
        if(session['user'] == 'admin'):
            c, conn = connectDB()
            
            return render_template('Database.html', members = members, memberscount = len(members))

        else:
            return redirect('/onlyformembers')
    else:
        return redirect('/onlyformembers')

@app.route('/sensitiveinfo')
def sensitiveinfo():
    return render_template("/privacy/sensitiveinfo.html")

# Start
if(__name__ == "__main__"):
    app.run()

'''
import MySQLdb
def connectDB():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="4swedu@skku", db="GBLD",charset="utf8mb4")
    c = conn.cursor()
    return c, conn

c, conn = connectDB()

'''
