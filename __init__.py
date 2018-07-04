
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

if(__name__ == "__main__"):
    app.run()
