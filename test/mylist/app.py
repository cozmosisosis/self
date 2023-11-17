from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("/main_template.html")

@app.route("/a")
def ahello_world():
    return "<p>AAAAAAAAAAAAAAAAA!</p>"