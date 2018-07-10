#-*- coding: utf-8-*-
#! /bin/usr/python
from error_code import*
from flask import Flask, render_template
from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = "HansClass"

# 입력 칸을 정의하는 클래스 선언
class LoginForm(Form):
    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])

class SignupForm(Form):
    name = StringField("name", validators=[InputRequired()])
    phone = StringField("phone", validators=[InputRequired()])
    email = StringField("email", validators=[InputRequired()])
    userid = StringField("username", validators=[InputRequired()])
    userpw = PasswordField("password", validators=[InputRequired()])
    pwconfirm = PasswordField("password", validators=[InputRequired()])
    school = StringField("school", validators=[InputRequired()])

class QuestionForm(Form):
    answer = StringField("answer")

# 데이터베이스에 연결하는 함수
def connection():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="4swedu@skku", db="GT_DB")
    c = conn.cursor()
    return c, conn

# Homepage
@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_Form = LoginForm()
    if(login_Form.validate_on_submit()):
        return "Login Successful"
    return render_template("/admin/login.html", form=login_Form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    c, conn = connection()
    signup_form = SignupForm()
    if(signup_form.validate_on_submit()):
        return "Sign Up Successful!"    

    return render_template("/admin/signup.html", form = signup_form)

@app.route("/leveltest")
def leveltest():
    questionNo = 0
    passfail = True
    # c,conn = connection() # DB에서 갖고와서 비교 후 값 전달    
    return render_template("/assessments/leveltest.html",QuestionNumber = questionNo, PassorFail = passfail)

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
    app.run(debug = True)
