import os, logging, sqlite3
from helpers import login_required, get_db, close_db
from flask import Flask, flash, render_template, redirect, session, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'





@app.route('/')
@login_required
def index():

    if 'user_id' in session:
        error = None
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE user_id = ?', (session['user_id'],))



        if user is None:
            error = "Failure retreving user account info please try logging on again"
            flash(error)
            return redirect(url_for('login'))

        db.execute('UPDATE users SET date_last_active = ? WHERE user_id = ?', (datetime.utcnow(), session['user_id']))
        db.commit()
        return render_template("index.html")

    error = 'login failure, user_id not found in session'
    flash(error)
    return redirect(url_for('login'))
    
        


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        if username == "" or password == "":
            error = 'Username and or Password was left empty'

        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()


        if user is None or not check_password_hash(user['hashed_password'], password):
            error = 'Username and or Password is Incorrect'

        if error is None:

            session.clear()
            session['user_id'] = user['user_id']
            try:
                db.execute('UPDATE users SET date_last_active = ? WHERE user_id = ?', (datetime.utcnow(), user['user_id']))
                db.commit()
                return redirect(url_for('index'))
            except:
                error = 'Failed to update date last active in account info'

        flash(error)
        return redirect(url_for('login'))
    else:
        try:
            if session['user_id'] is not None:
                flash('Logged in!')
                db = get_db()
                db.execute('UPDATE users SET date_last_active = ? WHERE user_id = ?', (datetime.utcnow(), session['user_id']))
                db.commit()
                return redirect(url_for('index'))
        except:
            return render_template('login.html')

        
    
    


@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session.clear()
    flash("Logged out")
    return redirect(url_for('login'))



@app.route("/register", methods=['POST', 'GET'])
def register():

    if request.method == 'GET':
        try:
            if session['user_id'] is not None:
                flash('Must not be logged in to register')
                return redirect(url_for('index'))
        except: pass

        return render_template('register.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_email = request.form.get('email',"None")
        password_verification = request.form['password_verification']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required'

        elif not password:
            error = 'Password is required'

        elif not password_verification:
            error = 'Second password is required'

        elif not password == password_verification:
            error = 'Passwords do not match'


        if error is None: 
            try:
                db.execute(
                    'INSERT INTO users (username, hashed_password, user_email, date_created, date_last_active) VALUES (?, ?, ?, ?, ?)',
                    (username, generate_password_hash(password), user_email, datetime.utcnow(), datetime.utcnow())
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            
            else:
                flash('Account created, Please Login!')
                return redirect(url_for('login'))


        flash(error)


        return redirect(url_for('register'))



@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    if 'user_id' in session:
        error = None
        db = get_db()
        user = db.execute('SELECT user_id, username, user_email, date_created, date_last_active FROM users WHERE user_id = ?', (session['user_id'],))

        if user is None:
            error = "Failure retreving user account info please try logging on again"
            flash(error)
            return redirect(url_for('login'))

        db.execute('UPDATE users SET date_last_active = ? WHERE user_id = ?', (datetime.utcnow(), session['user_id']))
        db.commit()
        return render_template("account.html", user=user)

    

@app.route("/my_items", methods=['GET', 'POST'])
@login_required
def my_items():

    if request.method == 'GET':
        # render db info
        db = get_db()
        item = db.execute("SELECT * FROM item WHERE user_id = ?", (session['user_id'],))
        return render_template('my_items.html', item=item)
        
    if not request.form['item_name']:
        flash('Name must be filled out to submit')
        return redirect(url_for('my_items'))

    new_item_name = request.form['item_name']
    db = get_db()
    db.execute("INSERT INTO item (user_id, item_name) VALUES (?, ?)", (session['user_id'], new_item_name, ))
    db.commit()
    return redirect(url_for('my_items'))
    
    

@app.route("/remove_item", methods=['GET', 'POST'])
@login_required
def remove_item():
    if request.method == 'GET':
        return redirect(url_for('my_items'))
    
    item_deleting = request.form['item_id']
    db = get_db()
    db.execute("DELETE FROM item WHERE item_id = ? AND user_id = ?", (item_deleting, session['user_id']))
    db.commit()
    return redirect(url_for('my_items'))



@app.route("/my_groups", methods=['GET', 'POST'])
@login_required
def my_groups():
    if request.method == 'GET':
        db = get_db()
        group_items = db.execute("SELECT groups.groups_name, item.item_name, groups_items.quantity FROM groups_items JOIN item ON groups_items.item_id = item.item_id JOIN groups ON groups.groups_id=groups_items.groups_id")
        group_items = list(group_items)
        groups = db.execute("SELECT * FROM groups WHERE user_id = ?", (session['user_id'],))
        return render_template('my_groups.html', groups=groups, group_items=group_items)
    new_group = request.form['group_name']
    
    if not new_group:
        flash('Group Name Not Filled out!')
        return redirect(url_for('my_groups'))
    
    db = get_db()
    group = db.execute("SELECT * FROM groups WHERE groups_name = ?", (new_group,)).fetchone()

    if group is not None:
        flash('Group already exists')
        return redirect(url_for('my_groups'))

    db.execute("INSERT INTO groups (user_id, groups_name) VALUES (?,?)", (session['user_id'], new_group))  
    db.commit()

    flash('Group Added')
    return redirect(url_for('my_groups'))



@app.route("/remove_group", methods=['GET', 'POST'])
@login_required
def remove_group():
    if request.method == 'GET':
        return redirect(url_for('my_groups'))
    group_deleting = request.form['groups_id']
    db = get_db()
    db.execute("DELETE FROM groups WHERE groups_id = ? AND user_id = ?", (group_deleting, session['user_id']))
    db.commit()
    return redirect(url_for('my_groups'))



@app.route("/edit_groups", methods=['GET', 'POST'])
@login_required
def edit_groups():
    if request.method == 'GET':
        db = get_db()


        groups = db.execute("SELECT * FROM groups WHERE user_id = ?", (session['user_id'],))
        groups = list(groups)
        group_items = db.execute("SELECT groups.groups_name, item.item_name, groups_items.quantity FROM groups_items JOIN item ON groups_items.item_id = item.item_id JOIN groups ON groups.groups_id=groups_items.groups_id")
        group_items = list(group_items)
        users_items = db.execute("SELECT * FROM item WHERE user_id = ?", (session['user_id'],))
        users_items = list(users_items)


        return render_template('edit_groups.html', groups=groups, group_items=group_items, users_items=users_items)
    return redirect(url_for('edit_groups'))



@app.route("/add_to_group", methods=['POST', 'GET'])
@login_required
def add_to_group():

    if request.method == 'GET':
        return redirect(url_for('edit_groups'))
    
    selected_group = request.form.get('groups')
    selected_item = request.form.get('items')
    quantity = request.form.get('quantity')
    quantity = int(quantity)


    if not selected_group or not selected_item or quantity <= 0:
        flash('Must select group, item to add and a valid quantity (greater than 0)')
        app.logger.error(selected_group)
        return redirect(url_for('edit_groups'))
    
    db = get_db()
    users_item = db.execute("SELECT * FROM item WHERE item_id = ? and user_id = ?", (selected_item, session['user_id'],)).fetchone()
    users_group = db.execute("SELECT * FROM groups WHERE groups_id = ? and user_id = ?", (selected_group, session['user_id'],)).fetchone()
    
    if users_item is None or users_group is None:
        flash('Error occured with either item submitted or group submitted to. No link to user')
        return redirect(url_for('edit_groups'))
    
    db.execute("INSERT INTO groups_items (groups_id, item_id, quantity) VALUES (?, ?, ?)", (selected_group, selected_item, 1))
    db.commit()
    return redirect(url_for('edit_groups'))



@app.errorhandler(404)
def page_not_found(error):
    flash('Invalid route')
    return redirect(url_for('index'))