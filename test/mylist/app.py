from flask import Flask, flash, render_template, redirect, sessions, request

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    return render_template("login.html")
        

@app.route("/a")
def a():
    return "<p>AAAAAAAAAAAAAAAAA!</p>"

@app.errorhandler(404)
def page_not_found(error):
    flash('Not a valid path. Sorry! But Anyways   ')
    return redirect("/")