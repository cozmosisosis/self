import os, logging, sqlite3
from datetime import datetime
from helpers import login_required, get_db, close_db
from flask import Flask, flash, jsonify, render_template, redirect, session, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'





@app.route('/')
@login_required
def index():

    db = get_db()

    if 'user_id' in session:
        error = None
        user = db.execute('SELECT * FROM users WHERE user_id = ?', (session['user_id'],)).fetchone()

        if not user:
            error = "Failure retreving user account info please try logging on again"
            flash(error)
            close_db()
            return redirect(url_for('login'))
        users_groups = list(db.execute("SELECT * FROM groups WHERE user_id = ?", (session['user_id'],)))
        users_items = list(db.execute("SELECT * FROM item WHERE user_id = ? ORDER BY item_name", (session['user_id'],)))
        user_active_items = list(db.execute("SELECT * FROM user_active_items JOIN item ON user_active_items.item_id = item.item_id WHERE user_active_items.user_id = ? ORDER BY item.item_name", (session['user_id'],)))
        
        db.execute('UPDATE users SET date_last_active = ? WHERE user_id = ?', (datetime.utcnow(), session['user_id']))
        db.commit()
        close_db()
        return render_template("index.html", users_items=users_items, user_active_items=user_active_items, users_groups=users_groups)

    error = 'login failure, user_id not found in session'
    flash(error)
    close_db()
    return redirect(url_for('login'))
    

    
@app.route('/add_to_active_list_individual', methods=['POST', 'GET'])
@login_required
def add_to_active_list_individual():

    db = get_db()

    if request.method == 'GET':
        close_db()
        return redirect(url_for('index'))

    item_to_add = request.form['item_to_add'].strip()
    quantity_to_add = request.form['quantity']
    quantity_to_add_int = int(quantity_to_add)
    if not item_to_add or not quantity_to_add or quantity_to_add_int < 1:
        flash('Input must not be empty and quantity must be valid')
        close_db()
        return redirect(url_for('index'))

    valid_item = db.execute("SELECT * FROM item WHERE user_id = ? AND item_name = ? COLLATE NOCASE", (session['user_id'], item_to_add,)).fetchone()
    if not valid_item:
        # case where item did not previously exist
        db.execute("INSERT INTO item (user_id, item_name) VALUES (?, ?)", (session['user_id'], item_to_add,))
        db.commit()
        new_item = db.execute("SELECT * FROM item WHERE user_id = ? AND item_name = ?", (session['user_id'], item_to_add)).fetchone()
        db.execute("INSERT INTO user_active_items (user_id, item_id, active_items_quantity) VALUES (?, ?, ?)", (session['user_id'], new_item['item_id'], quantity_to_add_int,))
        db.commit()
        close_db()
        return redirect(url_for('index'))

    item_on_list = db.execute("SELECT * FROM user_active_items WHERE user_id = ? AND item_id = ? AND groups_id IS NULL", (session['user_id'], valid_item['item_id'], )).fetchone()
    if item_on_list:
        new_quantity = item_on_list['active_items_quantity'] + quantity_to_add_int
        db.execute("UPDATE user_active_items SET active_items_quantity = ? WHERE user_id = ? AND item_id = ?", (new_quantity, session['user_id'], valid_item['item_id'],))
        db.commit()
        close_db()
        return redirect(url_for('index'))

    db.execute("INSERT INTO user_active_items (user_id, item_id, active_items_quantity) VALUES (?, ?, ?)", (session['user_id'], valid_item['item_id'], quantity_to_add_int))
    db.commit()
    close_db()
    return redirect(url_for('index'))



@app.route('/add_from_group', methods=['POST', 'GET'])
@login_required
def add_from_group():

    db = get_db()

    if request.method == 'GET':
        close_db()
        return redirect(url_for('edit_groups'))
    
    items = request.form
    for key in items:
        if key != 'groups_id':
            
            valid_item = db.execute("SELECT * FROM item WHERE user_id = ? AND item_id = ?", (session['user_id'], key,)).fetchone()
            if not valid_item:
                flash('Invalid Item in submission')
                close_db()
                return redirect(url_for('edit_groups'))
            if int(items[key]) < 0:
                flash('Invalid quantity in submission. Quantity can not be less than 0')
                close_db()
                return redirect(url_for('edit_groups'))
        else:
            groups_id = items[key]


    for key in items:
        if key != 'groups_id':

            item_in_list = db.execute("SELECT * FROM user_active_items WHERE user_id = ? AND item_id = ? AND groups_id = ?", (session['user_id'], key, groups_id)).fetchone()

            if int(items[key]) != 0:
                if not item_in_list:
                    db.execute("INSERT INTO user_active_items (user_id, item_id, groups_id, active_items_quantity) VALUES (?, ?, ?, ?)", (session['user_id'], key, groups_id, int(items[key])))
                    db.commit()
                else:
                    new_quantity = int(items[key]) + item_in_list['active_items_quantity']
                    db.execute("UPDATE user_active_items SET active_items_quantity = ? WHERE user_id = ? AND item_id = ? AND groups_id = ?", (new_quantity, session['user_id'], key, groups_id))
                    db.commit()

            
    close_db()
    flash('items added')
    return redirect(url_for('index'))



@app.route('/add_from_group_verification', methods=['POST', 'GET'])
@login_required
def add_from_group_verification():

    if request.method == 'GET':
        return redirect(url_for('edit_groups'))
    group_id = request.form.get('group_id')

    if not group_id:
        flash('Error with group id')
        return redirect(url_for('edit_groups'))

    db = get_db()
    
    valid_group = db.execute("SELECT * FROM groups WHERE user_id = ? AND groups_id = ?", (session['user_id'], group_id)).fetchone()
    if not valid_group:
        flash('Invalid Group')
        close_db()
        return redirect(url_for('edit_groups'))
    groups_items = list(db.execute("SELECT * FROM groups_items JOIN item ON groups_items.item_id = item.item_id WHERE groups_id = ?", (group_id,)))
    close_db()
    app.logger.error(len(groups_items))

    if len(groups_items) == 0:
        flash('Group has no items')
        return redirect(url_for('edit_groups'))
    
    return render_template('add_from_group_verification.html', groups_items=groups_items)



@app.route('/remove_from_active_list', methods=['GET', 'POST'])
@login_required
def remove_from_active_list():

    db = get_db()

    if request.method == 'GET':
        flash('Invalid route')
        close_db()
        return redirect(url_for('index'))
    
    active_item_removing = request.form['user_active_items_id']
    app.logger.error(active_item_removing)
    if not active_item_removing:
        flash('Error removing item, please try again')
        close_db()
        return redirect(url_for('index'))
    
    valid_active_item = db.execute("SELECT * FROM user_active_items WHERE user_id = ? AND user_active_items_id = ?", (session['user_id'], active_item_removing)).fetchone()
    if not valid_active_item:
        flash('Invalid item to remove please try again')
        close_db()
        return redirect(url_for('index'))
    db.execute("DELETE FROM user_active_items WHERE user_id = ? AND user_active_items_id = ?", (session['user_id'], active_item_removing,))
    db.commit()
    close_db()

    return redirect(url_for('index'))



@app.route('/change_quantity_on_active_list', methods=['GET', 'POST'])
@login_required
def change_quantity_on_active_list():

    db = get_db()
    if request.method == 'GET':
        return redirect(url_for('index'))
    
    item_id = request.form['item_id']
    new_quantity = request.form['new_quantity']
    new_quantity_int = int(new_quantity)

    if not item_id or not new_quantity or new_quantity_int < 0:
        flash('Invalid input')
        return redirect(url_for('index'))
    
    valid_item = db.execute("SELECT * FROM user_active_items WHERE user_id = ? AND item_id = ?", (session['user_id'], item_id,)).fetchone()
    if not valid_item:
        flash('Error invalid item')
        close_db()
        return redirect(url_for('index'))
    
    if new_quantity_int == 0:
        db.execute("DELETE FROM user_active_items WHERE user_id = ? AND item_id = ?", (session['user_id'], item_id,))
        db.commit()
        close_db()
        flash('Item quantity set to 0, Item removed')
        return redirect(url_for('index'))
    db.execute("UPDATE user_active_items SET active_items_quantity = ? WHERE user_id = ? AND item_id = ?", (new_quantity_int, session['user_id'], item_id,))
    db.commit()
    close_db()
    flash('quantity updated')
    return redirect(url_for('index'))



@app.route('/login', methods=['GET', 'POST'])
def login():

    db = get_db()

    if request.method == 'GET':

        if 'user_id' in session:
            app.logger.error('testing')
                    
            session_user_id_valid = db.execute("SELECT * FROM users WHERE user_id = ?", (session['user_id'],)).fetchone()
            if session_user_id_valid is None:
                session.clear()
                close_db()
                return render_template('login.html')
            flash('Logged in!')
            db.execute('UPDATE users SET date_last_active = ? WHERE user_id = ?', (datetime.utcnow(), session['user_id']))
            db.commit()
            close_db()
            return redirect(url_for('index'))
        else:
            close_db()
            return render_template('login.html')



    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        if username == "" or password == "":
            error = 'Username and or Password was left empty'

        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()


        if user is None or not check_password_hash(user['hashed_password'], password):
            error = 'Username and or Password is Incorrect'

        if error is None:

            session.clear()
            session['user_id'] = user['user_id']
            try:
                db.execute('UPDATE users SET date_last_active = ? WHERE user_id = ?', (datetime.utcnow(), user['user_id']))
                db.commit()
                close_db()
                return redirect(url_for('index'))
            except:
                error = 'Failed to update date last active in account info'

        flash(error)
        close_db()
        return redirect(url_for('login'))






@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session.clear()
    flash("Logged out")
    return redirect(url_for('login'))



@app.route("/register", methods=['POST', 'GET'])
def register():

    db = get_db()
    if request.method == 'GET':
        try:
            if session['user_id'] is not None:
                flash('Must not be logged in to register')
                close_db()
                return redirect(url_for('index'))
        except: pass
        close_db()
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_verification = request.form['password_verification']
        user_email = request.form['email']
        user_email_verification = request.form['email_verification']
        error = None

        if not username or not password or not password_verification:
            error = 'Please fill out all required fields'
        elif not password == password_verification:
            error = 'Passwords do not match'
        elif not user_email:
            user_email = None
        elif not user_email == user_email_verification:
            error = 'Email and email verification do not match!'


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
                if not user_email:
                    flash('Please update email for account recovery.')
                flash('Account created, Please Login!')
                close_db()
                return redirect(url_for('login'))


        flash(error)

        close_db()
        return redirect(url_for('register'))



@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    db = get_db()
    if 'user_id' in session:
        error = None
        user = db.execute('SELECT user_id, username, user_email, date_created, date_last_active FROM users WHERE user_id = ?', (session['user_id'],))

        if user is None:
            error = "Failure retreving user account info please try logging on again"
            flash(error)
            close_db()
            return redirect(url_for('login'))

        db.execute('UPDATE users SET date_last_active = ? WHERE user_id = ?', (datetime.utcnow(), session['user_id']))
        db.commit()
        close_db()
        return render_template("account.html", user=user)

    

@app.route("/my_items", methods=['GET', 'POST'])
@login_required
def my_items():

    db = get_db()
    if request.method == 'GET':
        # render db info
        item = db.execute("SELECT * FROM item WHERE user_id = ? ORDER BY item_name", (session['user_id'],))
        item = list(item)
        close_db()
        return render_template('my_items.html', item=item)
        
    if not request.form['item_name']:
        flash('Name must be filled out to submit')
        close_db()
        return redirect(url_for('my_items'))

    new_item_name = request.form['item_name'].strip()
    item_exists = db.execute("SELECT * FROM item WHERE item_name = ? AND user_id = ?", (new_item_name, session['user_id'],)).fetchone()
    if item_exists:
        flash('Item already exists')
        close_db()
        return redirect(url_for('my_items'))
    db.execute("INSERT INTO item (user_id, item_name) VALUES (?, ?)", (session['user_id'], new_item_name, ))
    db.commit()
    close_db()
    return redirect(url_for('my_items'))
    
    

@app.route("/remove_item", methods=['GET', 'POST'])
@login_required
def remove_item():

    db = get_db()
    if request.method == 'GET':
        close_db()
        return redirect(url_for('my_items'))
    
    item_deleting = request.form['item_id']

    valid_item = db.execute("SELECT * FROM item WHERE item_id = ? AND user_id = ?", (item_deleting, session['user_id'],)).fetchone()
    if not valid_item:
        flash('not valid item')
        close_db()
        return redirect(url_for('my_items'))

    db.execute("DELETE FROM item WHERE item_id = ? AND user_id = ?", (item_deleting, session['user_id']))
    db.commit()

    close_db()
    return redirect(url_for('my_items'))



@app.route("/change_item_name", methods=['GET', 'POST'])
@login_required
def change_item_name():

    db = get_db()
    if request.method == 'GET':
        close_db()
        return redirect(url_for('my_items'))
    
    item_id = request.form.get('item_id')
    item_new_name = request.form.get('item_new_name')

    if not item_id or not item_new_name:
        flash('Item must be chosen and a new name must be submitted to change an items name')
        close_db()
        return redirect(url_for('my_items'))

    valid_item = db.execute("SELECT * FROM item WHERE item_id = ? AND user_id = ?", (item_id, session['user_id'],)).fetchone()
    if not valid_item:
        flash('Error Invalid submission')
        close_db()
        return redirect(url_for('my_items'))

    if valid_item['item_name'] == item_new_name:
        flash('New item name is the same as old')
        close_db()
        return redirect(url_for('my_items'))

    db.execute("UPDATE item SET item_name = ? WHERE item_id = ? AND user_id = ?", (item_new_name, item_id, session['user_id'],))
    db.commit()

    close_db()
    flash('Item name changed')
    return redirect(url_for('my_items'))



@app.route("/my_groups", methods=['GET', 'POST'])
@login_required
def my_groups():

    db = get_db()
    if request.method == 'GET':
        groups = db.execute("SELECT * FROM groups WHERE user_id = ? ORDER BY groups_name", (session['user_id'],))
        groups = list(groups)
        close_db()
        return render_template('my_groups.html', groups=groups)
    new_group = request.form['group_name'].strip()
    
    if not new_group:
        flash('Group Name Not Filled out!')
        close_db()
        return redirect(url_for('my_groups'))
    
    group = db.execute("SELECT * FROM groups WHERE groups_name = ? AND user_id = ?", (new_group, session['user_id'],)).fetchone()

    if group is not None:
        flash('Group already exists')
        close_db()
        return redirect(url_for('my_groups'))

    db.execute("INSERT INTO groups (user_id, groups_name) VALUES (?,?)", (session['user_id'], new_group))  
    db.commit()

    flash('Group Added')
    close_db()
    return redirect(url_for('my_groups'))



@app.route("/remove_group", methods=['GET', 'POST'])
@login_required
def remove_group():

    db = get_db()
    if request.method == 'GET':
        close_db()
        return redirect(url_for('my_groups'))
    group_deleting = request.form['groups_id']
    valid_group = db.execute("SELECT * FROM groups WHERE groups_id = ? AND user_id = ?", (group_deleting, session['user_id'],)).fetchone()
    if not valid_group:
        flash('Error with trying to delete group')
        close_db()
        return redirect(url_for('my_groups'))
    
    db.execute("DELETE FROM groups WHERE groups_id = ? AND user_id = ?", (group_deleting, session['user_id']))
    db.commit()
    close_db()
    return redirect(url_for('my_groups'))



@app.route("/change_group_name", methods=['GET', 'POST'])
@login_required
def change_group_name():

    db = get_db()
    if request.method == 'GET':
        flash('invalid method')
        close_db()
        return redirect(url_for('my_groups'))
    
    groups_id = request.form.get('groups_id_for_name_change')
    groups_new_name = request.form.get('groups_new_name')

    if not groups_id or not groups_new_name:
        flash('Must select and fill out all of form before submitting')
        close_db()
        return redirect(url_for('my_groups'))

    valid_group = db.execute("SELECT * FROM groups WHERE groups_id = ? AND user_id = ?", (groups_id, session['user_id'],)).fetchone()
    if not valid_group:
        flash('Error Invalid submission')
        close_db()
        return redirect(url_for('my_groups'))

    if valid_group['groups_name'] == groups_new_name:
        flash('New name is the same as old')
        close_db()
        return redirect(url_for('my_groups'))

    db.execute("UPDATE groups SET groups_name = ? WHERE groups_id = ? AND user_id = ?", (groups_new_name, groups_id, session['user_id'],))
    db.commit()
    close_db()
    flash('changed group name')
    return redirect(url_for('my_groups'))



@app.route("/edit_groups", methods=['GET', 'POST'])
@login_required
def edit_groups():

    db = get_db()
    if request.method == 'GET':

        groups = list(db.execute("SELECT * FROM groups WHERE user_id = ? ORDER BY groups_name", (session['user_id'],)))
        group_items = list(db.execute("SELECT groups_items.groups_id, item.item_id, item.item_name, groups_items.quantity, item.user_id FROM item JOIN groups_items ON groups_items.item_id = item.item_id WHERE item.user_id = ? ORDER BY item_name", (session['user_id'],)))
        users_items = list(db.execute("SELECT * FROM item WHERE user_id = ? ORDER BY item_name", (session['user_id'],)))

        close_db()
        return render_template('edit_groups.html', groups=groups, group_items=group_items, users_items=users_items)
    close_db()
    return redirect(url_for('edit_groups'))



@app.route("/add_to_group", methods=['POST', 'GET'])
@login_required
def add_to_group():

    db = get_db()
    if request.method == 'GET':
        close_db()
        return redirect(url_for('edit_groups'))
    
    selected_group = request.form.get('groups')
    selected_item = request.form.get('items')
    inputed_quantity = request.form.get('quantity')


    if not selected_group or not selected_item or not inputed_quantity:
        flash('Must select group, item to add and a valid quantity (greater than 0)')
        close_db()
        return redirect(url_for('edit_groups'))
    
    inputed_quantity = int(inputed_quantity)
    if inputed_quantity <= 0:
        flash('Must input a valid quantity (greater than 0)')
        close_db()
        return redirect(url_for('edit_groups'))


    users_item = db.execute("SELECT * FROM item WHERE item_id = ? and user_id = ?", (selected_item, session['user_id'],)).fetchone()
    users_group = db.execute("SELECT * FROM groups WHERE groups_id = ? and user_id = ?", (selected_group, session['user_id'],)).fetchone()
    
    if users_item is None or users_group is None:
        flash('Error occured with either item submitted or group submitted to. No link to user')
        close_db()
        return redirect(url_for('edit_groups'))
    
    ingredient_is_in_groups_items = db.execute("SELECT * FROM groups_items WHERE groups_id = ? AND item_id = ?", (selected_group, selected_item,)).fetchone()

    if not ingredient_is_in_groups_items:
        db.execute("INSERT INTO groups_items (groups_id, item_id, quantity) VALUES (?, ?, ?)", (selected_group, selected_item, inputed_quantity))
        db.commit()
        close_db()
        return redirect(url_for('edit_groups'))

    old_quantity = ingredient_is_in_groups_items['quantity']
    new_quantity = inputed_quantity + old_quantity
    db.execute("UPDATE groups_items SET quantity = ? WHERE groups_id = ? AND item_id = ?", (new_quantity, selected_group, selected_item,))
    db.commit()
    close_db()
    return redirect(url_for('edit_groups'))







@app.route("/remove_from_group", methods=['POST', 'GET'])
@login_required
def remove_from_group():

    db = get_db()

    item_to_remove = request.form['item_id']
    group_removing_from = request.form['groups_id']

    valid_item = db.execute("SELECT * FROM item WHERE item_id = ? AND user_id = ?", (item_to_remove, session['user_id'],)).fetchone()
    valid_group = db.execute("SELECT * FROM groups WHERE groups_id = ? and user_id = ?", (group_removing_from, session['user_id'],)).fetchone()
    if not valid_item or not valid_group:
        flash('not valid item or group')
        close_db()
        return redirect(url_for('edit_groups'))

    app.logger.error(item_to_remove)
    app.logger.error(group_removing_from)
    db.execute("DELETE FROM groups_items WHERE groups_id = ? AND item_id = ?", (group_removing_from, item_to_remove,))
    db.commit()
    close_db()
    flash('item removed from group')
    return redirect(url_for('edit_groups'))



@app.route("/delete_account", methods=['GET', 'POST'])
@login_required
def delete_account():

    db = get_db()
    if request.method == 'GET':
        close_db()
        return render_template('delete_account.html')
    
    username = request.form['username']
    password = request.form['password']

    if not username or not password:
        flash('Must fill out both username and password to DELETE account')
        close_db()
        return redirect(url_for('delete_account'))
    
    user = db.execute('SELECT * FROM users WHERE user_id = ?', (session['user_id'],)).fetchone()


    if user is None or username != user['username'] or not check_password_hash(user['hashed_password'], password):
        flash('Error with submitted User Info for deletion. Please log out, log back in, and then try deleting account again.')
        close_db()
        return redirect(url_for('delete_account'))



    db.execute("DELETE FROM users WHERE user_id = ?", (session['user_id'],))

    db.commit()
    close_db()

    session.clear()
    flash("Account Deleted")
    return redirect(url_for('login'))



@app.route("/edit_account", methods=['POST', 'GET'])
@login_required
def edit_account():
    
    if request.method == 'GET':
        return render_template('edit_account.html')
    
    flash('post to edit account')    
    return redirect(url_for('account'))



@app.route("/edit_account/<info_to_edit>", methods=['POST', 'GET'])
@login_required
def edit_account_route(info_to_edit):

    db = get_db()
    valid_routes = ['username', 'password', 'email']

    if info_to_edit not in valid_routes:
        flash('Invalid info to edit')
        return redirect(url_for('edit_account'))
    
    if request.method == 'GET':
        return render_template('edit_account_route.html', info_to_edit=info_to_edit)
        
    if request.method == 'POST':

        value_edditing = request.form['value_edditing']
        new_value = request.form['new_value']
        current_username = request.form['current_username']
        current_password = request.form['current_password']

        if not new_value or not current_password or not current_username:
            flash('All Fields must be filled out')
            return redirect(f'/edit_account/{info_to_edit}')
        
        user = db.execute("SELECT * FROM users WHERE user_id = ?", (session['user_id'],)).fetchone()


        if current_username != user['username'] or not check_password_hash(user['hashed_password'], current_password) or session['user_id'] != user['user_id']:
            flash('Account not verified, please try again')
            close_db()
            return redirect(f'/edit_account/{info_to_edit}')


        if value_edditing == 'username':
            if user['username'] == new_value:
                flash('Inputed new username is the same as old username')
                close_db()
                return redirect(f'/edit_account/{info_to_edit}')
            db.execute("UPDATE users SET username = ? WHERE user_id = ?", (new_value, session['user_id'],))
        elif value_edditing == 'password':
            value_edditing = 'hashed_password'
            if check_password_hash(user['hashed_password'], new_value):
                flash('Inputed new password is the same as old password')
                close_db()
                return redirect(f'/edit_account/{info_to_edit}')
            db.execute("UPDATE users SET hashed_password = ? WHERE user_id = ?", ( generate_password_hash(new_value), session['user_id'],))
        elif value_edditing == 'email':
            value_edditing = 'user_email'
            if user['user_email'] == new_value:
                flash('Inputed new email is the same as old email')
                close_db()
                return redirect(f'/edit_account/{info_to_edit}')
            try:
                db.execute("UPDATE users SET user_email = ? WHERE user_id = ?", (new_value, session['user_id'],))
            except:
                flash('Unable to add email, email already associated with an account')

        db.commit()
        close_db()
        return redirect(url_for('account'))





@app.route('/change_quantity_in_group', methods=['POST', 'GET'])
@login_required
def change_quantity_in_group():

    db = get_db()


    groups_items_id = request.args.get('id')
    value = request.args.get('value')

    valid_groups_item = db.execute("SELECT * FROM groups_items JOIN groups ON groups_items.groups_id = groups.groups_id WHERE groups.user_id = ? AND groups_items.groups_items_id = ?", (session['user_id'], groups_items_id)).fetchone()
    if not valid_groups_item:
        groups = list(db.execute("SELECT * FROM groups WHERE user_id = ? ORDER BY groups_name", (session['user_id'],)))
        group_items = list(db.execute("SELECT groups_items.groups_id, item.item_id, item.item_name, groups_items.quantity, item.user_id, groups_items.groups_items_id FROM item JOIN groups_items ON groups_items.item_id = item.item_id WHERE item.user_id = ? ORDER BY item_name", (session['user_id'],)))
        users_items = list(db.execute("SELECT * FROM item WHERE user_id = ? ORDER BY item_name", (session['user_id'],)))
        close_db()
        return jsonify(render_template('ajax_edit_groups.html', groups=groups, group_items=group_items, users_items=users_items))

    value = int(value)
    if value > 0:
        db.execute("UPDATE groups_items SET quantity = ? WHERE groups_items_id = ?", (value, groups_items_id,))
        db.commit()
        groups = list(db.execute("SELECT * FROM groups WHERE user_id = ? ORDER BY groups_name", (session['user_id'],)))
        group_items = list(db.execute("SELECT groups_items.groups_id, item.item_id, item.item_name, groups_items.quantity, item.user_id, groups_items.groups_items_id FROM item JOIN groups_items ON groups_items.item_id = item.item_id WHERE item.user_id = ? ORDER BY item_name", (session['user_id'],)))
        users_items = list(db.execute("SELECT * FROM item WHERE user_id = ? ORDER BY item_name", (session['user_id'],)))
        close_db()
        return jsonify(render_template('ajax_edit_groups.html', groups=groups, group_items=group_items, users_items=users_items))

    else:
        db.execute("DELETE FROM groups_items WHERE groups_items_id = ?", (groups_items_id,))
        db.commit()
        groups = list(db.execute("SELECT * FROM groups WHERE user_id = ? ORDER BY groups_name", (session['user_id'],)))
        group_items = list(db.execute("SELECT groups_items.groups_id, item.item_id, item.item_name, groups_items.quantity, item.user_id, groups_items.groups_items_id FROM item JOIN groups_items ON groups_items.item_id = item.item_id WHERE item.user_id = ? ORDER BY item_name", (session['user_id'],)))
        users_items = list(db.execute("SELECT * FROM item WHERE user_id = ? ORDER BY item_name", (session['user_id'],)))
        close_db()
        return jsonify(render_template('ajax_edit_groups.html', groups=groups, group_items=group_items, users_items=users_items))







@app.route('/ajax_test')
@login_required
def ajax_test():

    db = get_db()

    if 'user_id' in session:
        error = None
        user = db.execute('SELECT * FROM users WHERE user_id = ?', (session['user_id'],)).fetchone()

        if not user:
            error = "Failure retreving user account info please try logging on again"
            flash(error)
            close_db()
            return redirect(url_for('login'))
        users_groups = list(db.execute("SELECT * FROM groups WHERE user_id = ?", (session['user_id'],)))
        users_items = list(db.execute("SELECT * FROM item WHERE user_id = ? ORDER BY item_name", (session['user_id'],)))
        user_active_items = list(db.execute("SELECT * FROM user_active_items JOIN item ON user_active_items.item_id = item.item_id WHERE user_active_items.user_id = ? ORDER BY item.item_name", (session['user_id'],)))
        
        db.execute('UPDATE users SET date_last_active = ? WHERE user_id = ?', (datetime.utcnow(), session['user_id']))
        db.commit()
        close_db()
        return render_template("ajax_test.html", users_items=users_items, user_active_items=user_active_items, users_groups=users_groups)

    error = 'login failure, user_id not found in session'
    flash(error)
    close_db()
    return redirect(url_for('login'))


@app.route('/ajax_test_submit', methods=['GET', 'POST'])
@login_required
def ajax_test_submit():

    db = get_db()
    if request.method == 'GET':
        app.logger.error('Method is get')
        users_groups = list(db.execute("SELECT * FROM groups WHERE user_id = ?", (session['user_id'],)))
        users_items = list(db.execute("SELECT * FROM item WHERE user_id = ? ORDER BY item_name", (session['user_id'],)))
        user_active_items = list(db.execute("SELECT * FROM user_active_items JOIN item ON user_active_items.item_id = item.item_id WHERE user_active_items.user_id = ? ORDER BY item.item_name", (session['user_id'],)))
        close_db()
        return jsonify(render_template('ajax_index.html', users_groups=users_groups, users_items=users_items, user_active_items=user_active_items))


    app.logger.error('Method is post')
    user_active_items_id = request.form.get('id')
    value = request.form.get('value')
    if not value or not user_active_items_id or type(int(value)) is not int or not int(user_active_items_id):
        app.logger.error('error with values')
        return redirect(url_for('ajax_test_submit'))


    value = int(value)
    user_active_items_id = int(user_active_items_id)
    valid_user_active_items = db.execute("SELECT * FROM user_active_items WHERE user_id = ? AND user_active_items_id = ?", (session['user_id'], user_active_items_id)).fetchone()

    if not valid_user_active_items:
        app.logger.error('invalid active item')
        return redirect(url_for('ajax_test_submit'))
        

    if value > 0:
        db.execute("UPDATE user_active_items SET active_items_quantity = ? WHERE user_active_items_id = ?", (value, user_active_items_id))
        db.commit()
        return redirect(url_for('ajax_test_submit'))
    

        
    else:
        db.execute("DELETE FROM user_active_items WHERE user_active_items_id = ?", (user_active_items_id,))
        db.commit()
        return redirect(url_for('ajax_test_submit'))







@app.errorhandler(404)
def page_not_found(error):
    flash('Invalid route')
    return redirect(url_for('index'))