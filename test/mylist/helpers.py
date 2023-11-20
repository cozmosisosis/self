import os
from functools import wraps
from flask import Flask, flash, render_template, redirect, session, request, url_for



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            flash("No account with given username and password")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function