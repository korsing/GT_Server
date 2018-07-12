#-*- coding: utf-8-*-

from error_code import*
from flask import Flask, render_template
from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Email, Length
import MySQLdb

app = Flask(__name__)
app.config['SECRET_KEY'] = "HansClass"
app.debug = True

# 입력 칸을 정의하는 클래스 선언
class LoginForm(Form):
    userid = StringField("username", validators=[InputRequired()])
    passwd = PasswordField("password", validators=[InputRequired()])

class SignupForm(Form):
    name = StringField("name", validators=[InputRequired()])
    phone = StringField("phone", validators=[InputRequired(), Length(min=13, max=13)])
    email = StringField("email", validators=[InputRequired(), Email(message="Invalid Email")])
    userid = StringField("username", validators=[InputRequired()])
    userpw = PasswordField("password", validators=[InputRequired()])
    pwconfirm = PasswordField("password", validators=[InputRequired()])
    school = StringField("school", validators=[InputRequired()])

class QuestionForm(Form):
    answer = StringField("answer")


def connectDB():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="4swedu@skku", db="GT_DB",charset="utf8mb4")
    c = conn.cursor()
    return c, conn

# Homepage
@app.route('/')
def homepage():
    return render_template("index.html", name="NULL")

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if(login_form.validate_on_submit()):
        c, conn = connectDB()
        userid = login_form.userid.data
        userpw = login_form.userpw.data
        test = userid + ' ' + userpw
        return test
        #c.execute("SELECT userpw FROM USERS WHERE userid = %s", (userid,))
        #return c.fetchone()[0]
        #if(userpw == c.fetchone()[0]):
        #    return render_template("/index.html", name = login_form.name.data)
        #else:
        #    return "Login Fail!"
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
