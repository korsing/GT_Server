from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to Professor Han's Class!"


if(__name__ == "__main__"):
    app.run()
