#-*- coding: utf-8-*-
from flask import Flask, render_template, session, redirect, flash
from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Email, Length
import MySQLdb
import os
from werkzeug.security import generate_password_hash, check_password_hash


# Flask가 동작하기 위해서 필요한 기본 설정 들..
app = Flask(__name__)
app.config['SECRET_KEY'] = "HansClass"
app.secret_key = os.urandom(50)

# 초기 설문조사를 위한 클래스 선언
class SurveyForm(Form):
    answer = SelectField("answer", choices=[("option1", "혼자할래요"), ("option2", "같이할래요")], validators=[InputRequired()])

# 입력 칸을 정의하는 클래스 선언
class LoginForm(Form):
    userid = StringField("username", validators=[InputRequired()])
    userpw = PasswordField("password", validators=[InputRequired()])

# 회원가입란을 정의하는 클래스 선언
class SignupForm(Form):
    name = StringField("name", validators=[InputRequired()])
    phone = StringField("phone", validators=[InputRequired()])
    email = StringField("email", validators=[InputRequired()])
    userid = StringField("username", validators=[InputRequired()])
    userpw = PasswordField("password", validators=[InputRequired()])
    pwconfirm = PasswordField("password", validators=[InputRequired()])
    school = StringField("school", validators=[InputRequired()])

# 레벨테스트란을 정의하는 클래스 선언
class QuestionForm(Form):
    answer = TextAreaField("answer")

# DB 연동을 수행하는 함수
def connectDB():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="4swedu@skku", db="GT_DB",charset="utf8mb4")
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
        return render_template("index.html", name=name, flag = True)
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
        if(userpw_tuple==None): # 갖고온게 하나도 없다는 말은 userid가 존재하지 않는다!
            message = "Your ID or PASSWORD seems to be wrong!"
            createError(message)
            return redirect('/error')
        else:
            if(check_password_hash(userpw_tuple[0], login_form.userpw.data)): # 입력한 비밀번호와 DB상의 비밀번호가 같다면
                createSession(userid) # 로그인이 완료된 상황이니 세션을 생성
                return redirect('/')
            else: # 입력한 비밀번호가 DB와 다르다면
                message = "Your ID or PASSWORD seems to be wrong!"
                createError(message)
                return redirect('/error')
    return render_template("/admin/login.html", form=login_form)

@app.route('/onlyformembers')
def onlyformembers():
    return render_template("/admin/onlyformembers.html")

@app.route('/logout')
def logout():
    deleteSession()
    return redirect('/')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    if(signup_form.validate_on_submit()):
        if('@' not in signup_form.email.data):
            message = "Wrong EMAIL has been entered."
            createError(message)
            return redirect('/error')
            
        if(len(signup_form.userid.data) < 5):
            message = "ID must be more than 5 characters."
            createError(message)
            return redirect('/error')

        if(len(signup_form.userpw.data) < 8):
            message = "PASSWORD must be more than 8 characters."
            createError(message)
            return redirect('/error')

        if(signup_form.userpw.data != signup_form.pwconfirm.data): # 비밀번호와 비밀번호 확인이 일치하는지 체크
            message = "PASSWORDs do not match!"
            createError(message)
            return redirect('/error')

        c, conn = connectDB()
        c.execute("SELECT userid from USERS;")
        for userid_tuple in c.fetchall():
            if(signup_form.userid.data in userid_tuple): # DB에 이미 해당 아이디가 있다면
                message = "That ID already exists! Please another one."
                createError(message)
                return redirect('/error')
        
        # 이까지 온다는 것 자체가 위에 에러 if문에서 하나도 안걸렸다는 말!
        password = generate_password_hash(signup_form.userpw.data) 
        c.execute("INSERT INTO USERS VALUES (%s, %s, %s, %s, %s, %s)", (signup_form.name.data, signup_form.userid.data, password, signup_form.email.data, signup_form.phone.data, signup_form.school.data))
        conn.commit()
        conn.close()
        return redirect("/login")
    return render_template("/admin/signup.html", form = signup_form)

@app.route("/leveltest")
def leveltest():
    if('user' in session):
        userid = session['user']
        c, conn = connectDB()
        c.execute("SELECT name FROM USERS WHERE userid = %s", (userid,))
        name = c.fetchone()[0]
        return render_template("/assessments/leveltest.html", name = name, flag = True)
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

def get_CAT(qnum):
    if(qnum <= 25):
        category = "thinking"
    elif(qnum <= 50):
        category = "entry"
    elif(qnum <= 75):
        category = "python"
    elif(qnum <= 100):
        category = "c"
    else:
        category = 'intro'
    return category

@app.route("/leveltest/Q<qnum>", methods=['GET', 'POST'])
def questions(qnum):
    if('user' in session):
        userid = session['user']
        category = get_CAT(int(qnum))
        if(int(qnum) <= 100):
            form = QuestionForm()
        else:
            form = QuestionForm() #나중에 수정의 용이성을 위해서..
        if(form.validate_on_submit()): 
            data = form.answer.data
            if(len(data)>500):
                data = data[:500]
            c,conn = connectDB()
            query = "SELECT * FROM " + category + " WHERE userid = '" + userid + "';"
            flag = c.execute(query)
            if(flag != 0):
                update_Variable = "UPDATE " + category +" SET Q"+ str(qnum) +" = '" + data + "' WHERE userid = '" + userid + "';"
                c.execute(update_Variable)
            else:
                execute_Variable = "Insert into "+ category + " (userid, Q" + str(qnum) + " ) VALUES ('" + userid + "','" + data+ "');"
                c.execute(execute_Variable)
            conn.commit()
            conn.close()
            return redirect('/leveltest/' + category)
        return render_template("/assessments/questions/" + category +"/Q" + str(qnum) + ".html", form=form, flag = True)
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
                return render_template("/assessments/questions/" + variable + "/start.html", PassorFail=passorfail, difficulty = difficulty)
        else:
            return redirect("/onlyformembers")

@app.route('/dashboard')
def printdb():
    if('user' in session):
        if(session['user'] == 'admin'):
            c, conn = connectDB()
            userNo = c.execute("SELECT name, userid, email, phone FROM USERS")
            data = c.fetchall()
            members = []
            for userdata in data:
                for element in userdata:
                    members.append(element)
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
    conn = MySQLdb.connect(host="localhost", user="root", passwd="4swedu@skku", db="GT_DB",charset="utf8mb4")
    c = conn.cursor()
    return c, conn

c, conn = connectDB()

'''