import os, sqlite3, click
from functools import wraps
from flask import Flask, flash, render_template, redirect, session, request, url_for,current_app, g



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            flash("Not logged in")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function



def get_db():
    conn = sqlite3.connect('mylist.db')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn



def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()



