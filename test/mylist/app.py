from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World and all its people!</p>"

@app.route("/a")
def ahello_world():
    return "<p>AAAAAAAAAAAAAAAAA!</p>"