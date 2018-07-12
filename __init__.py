#-*- coding: utf-8-*-

from error_code import*
from flask import Flask, render_template, session
from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Email, Length
import MySQLdb
import os

# Flask가 동작하기 위해서 필요한 기본 설정 들..
app = Flask(__name__)
app.config['SECRET_KEY'] = "HansClass"
app.secret_key = os.urandom(50)

# 아래 클래스의 각 필드의 validator가 만족되지 않았을 때 띄워줄 메세지가 필요함
# 입력 칸을 정의하는 클래스 선언
class LoginForm(Form):
    userid = StringField("username", validators=[InputRequired()])
    userpw = PasswordField("password", validators=[InputRequired()])

# 회원가입란을 정의하는 클래스 선언
class SignupForm(Form):
    name = StringField("name", validators=[InputRequired()])
    phone = StringField("phone", validators=[InputRequired(), Length(min=13, max=13)])
    email = StringField("email", validators=[InputRequired(), Email(message="Invalid Email")])
    userid = StringField("username", validators=[InputRequired()])
    userpw = PasswordField("password", validators=[InputRequired()])
    pwconfirm = PasswordField("password", validators=[InputRequired()])
    school = StringField("school", validators=[InputRequired()])

# 레벨테스트란을 정의하는 클래스 선언
class QuestionForm(Form):
    answer = StringField("answer")

# DB 연동을 수행하는 함수
def connectDB():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="4swedu@skku", db="GT_DB",charset="utf8mb4")
    c = conn.cursor()
    return c, conn

# 홈페이지 # 로그인 없이는 각 버튼 접근 권한 없애야함!
@app.route('/')
def homepage():
    return render_template("index.html", name="NULL")

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if(login_form.validate_on_submit()): # 로그인 버튼이 눌렸을 때 수행되는 코드
        c, conn = connectDB() # DB에 연결하고
        userid = login_form.userid.data # 입력받은 아이디와
        userpw = login_form.userpw.data # 비밀번호를 저장
        c.execute("SELECT userpw FROM USERS WHERE userid = %s", (userid,)) # 아이디를 사용하여 비밀번호를 DB에서 가져옴
        if(userpw == c.fetchone()[0]): # 입력한 비밀번호와 DB상의 비밀번호가 같다면
            c.execute("SELECT name FROM USERS WHERE userid = %s", (userid,)) # DB에서 이름을 갖고온다.
            name = c.fetchone()[0]
            session['user'] = name
            return render_template("/index.html", name = name )
        else:
            return "Login Fail!"
    return render_template("/admin/login.html", form=login_form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    if(signup_form.validate_on_submit()):   
        c, conn = connectDB()
        c.execute("INSERT INTO USERS VALUES (%s, %s, %s, %s, %s, %s)", (signup_form.name.data, signup_form.userid.data, signup_form.userpw.data, signup_form.email.data, signup_form.phone.data, signup_form.school.data))
        conn.commit()
        conn.close()
        return render_template("/admin/login.html")
    return render_template("/admin/signup.html", form = signup_form)

@app.route("/leveltest")
def leveltest():
    questionNo = 0
    passfail = True
    return render_template("/assessments/leveltest.html", QuestionNumber = questionNo, PassorFail = passfail)

@app.route('/abouttest')
def aboutleveltest():
    return render_template("/assessments/abouttest.html")

@app.route("/leveltest/Q<qnum>")
def question(qnum):
    return render_template("/assessments/questions/question" + str(qnum) + ".html") # 테스트 필요

@app.route('/sensitiveinfo')
def sensitiveinfo():
    return render_template("/privacy/sensitiveinfo.html")

@app.route('/lecture')
def lecture():
    return render_template("lecture.html")

@app.route('/error<errcode>')
def error(errcode):
    return render_template("/admin/error.html", errcode=errcode)

# Start
if(__name__ == "__main__"):
    app.run()
