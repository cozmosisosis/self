from flask import Flask, render_template, redirect, sessions

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("/main_template.html")

@app.route("/a")
def a():
    return "<p>AAAAAAAAAAAAAAAAA!</p>"