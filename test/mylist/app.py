import os
import logging
from flask import Flask, flash, render_template, redirect, session, request

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
logged_in = False


@app.route("/", methods=['POST', 'GET'])
def index():

    if logged_in:
        return render_template("index.html")
    
    return redirect("/login")
        


@app.route("/registration", methods=['POST', 'GET'])
def registration():

    if request.method == 'GET':
        return render_template("registration.html")
    return redirect("/")



@app.route("/login", methods=['POST', 'GET'])
def login():

    if request.method == 'GET':
        return render_template("login.html")
    logged_in = True
    
    return redirect("/")



@app.errorhandler(404)
def page_not_found(error):

    flash('Not a valid path. Sorry! But Anyways   ')
    return redirect("/")