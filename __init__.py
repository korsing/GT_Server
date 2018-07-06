
#! /bin/usr/python
from flask import Flask, \
                  render_template, \
                  flash, \
                  redirect, \
                  url_for, \
                  session
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, BooleanField
# from wtforms.validators import InputRequired, Email, Length           
# import MySQLdb # Database Access
# from datetime import datetime 

app = Flask(__name__)

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember Me')



# Homepage
@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/login')
def login():
    form = LoginForm()

    return render_template("/admin/login.html", form = form)

@app.route("/signup")
def signup():
    return render_template("/admin/signup.html")

@app.route("/leveltest")
def leveltest():
    return render_template("/assessments/leveltest.html")

@app.route('/abouttest')
def aboutleveltest():
    return render_template("/assessments/abouttest.html")

@app.route('/sensitiveinfo')
def sensitiveinfo():
    return render_template("/privacy/sensitiveinfo.html")

@app.route('/lecture')
def lecture():
    return render_template("lecture.html")

@app.route('/error<errcode>')
def error(errcode):
    return render_template("error.html", errcode=errcode)

# Start
if(__name__ == "__main__"):
    app.run()
