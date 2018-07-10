
#! /bin/usr/python
from error_code import*
from flask import Flask, render_template

result = 10/0

app = Flask(__name__)
app.config['SECRET_KEY'] = "HansClass"

# Homepage
@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/login',)
def login():
    return render_template("/admin/login.html")

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
    app.run(debug = True)
