from flask import Flask, render_template

app = Flask(__name__)

# 홈페이지 (메인화면)
@app.route('/')
def index():
    return render_template('index.html')




@app.route("/profile/<name>")
def profile(name):
    return render_template("profile.html")

if(__name__ == "__main__"):
    app.run()
