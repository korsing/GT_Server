from flask import Flask, render_template, flash, redirect, url_for, session
from data import Articles

app = Flask(__name__)

# 홈페이지 (메인화면)
@app.route('/')
@app.route('/<user>')
def index(user=None):
    return render_template('index.html', user = user)

@app.route("/profile/<name>")
def profile(name):
    return render_template("profile.html", name = name)

if(__name__ == "__main__"):
    app.run()
