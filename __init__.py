
#! /bin/usr/python
from flask import Flask, render_template #, flash, redirect, url_for, session
# from data import Articles

app = Flask(__name__)

# Homepage
@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/leveltest")
def leveltest():
    return render_template("leveltest.html")

@app.route('/abouttest')
def aboutleveltest():
    return render_template("abouttest.html")

@app.route('/sensitiveinfo')
def sensitiveinfo():
    return render_template("sensitiveinfo.html")

@app.route('/lecture')
def lecture():
    return render_template("lecture.html")

if(__name__ == "__main__"):
    app.run()
