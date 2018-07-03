
#! /bin/usr/python
from flask import Flask #, render_template, flash, redirect, url_for, session
# from data import Articles

app = Flask(__name__)

# Homepage
@app.route('/')
def homepage():
    return "Bye There!!!"


# @app.route('/<user>')
# def index(user=None):
#    return render_template('index.html', user = user)



if(__name__ == "__main__"):
    app.run()
