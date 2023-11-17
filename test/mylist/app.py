from flask import Flask, flash, render_template, redirect, sessions, request

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
def index():
    return render_template("/index.html")

@app.route("/a")
def a():
    return "<p>AAAAAAAAAAAAAAAAA!</p>"

@app.errorhandler(404)
def page_not_found(error):
    flash('Not a valid path. Sorry! \nBut Anyways   ')
    return redirect("/")