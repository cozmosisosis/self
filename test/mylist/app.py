import os
import logging
from helpers import login_required
from flask import Flask, flash, render_template, redirect, session, request, url_for

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'




@app.route('/')
@login_required
def index():

    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are logged out...'
    
        


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    
    return render_template('login.html')
    


@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session.pop('username', None)
    flash("Logged out")
    return redirect(url_for('login'))



@app.route("/register", methods=['POST', 'GET'])
def register():

    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_verification = request.form['password_verification']
        error = None

        if not username:
            error = 'Username is required'

        elif not password:
            error = 'Password is required'

        elif not password_verification:
            error = 'Second password is required'

        elif not password == password_verification:
            error = 'Passwords do not match'

        flash(error)

        if error is None: 

            return redirect("/login")
            # try:
            #     create username


        return redirect(url_for('register'))




@app.errorhandler(404)
def page_not_found(error):

    return redirect(url_for('index'))