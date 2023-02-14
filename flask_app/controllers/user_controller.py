from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User

bcrypt = Bcrypt(app)

#Route to the landing page
@app.route('/')
def landing_page_route():
    if 'user_id' in session:
        return redirect('/home')
    return render_template('index.html')

@app.route('/login')
def login_route():
    if 'user_id' in session:
        return redirect('/home')
    return render_template('login.html')

#Route to the Logged In homepage
@app.route("/home")
def logged_in_homepage_route():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    logged_user = User.get_by_id(data)
    return render_template("home.html", logged_user=logged_user)

#A route to process my post data
@app.route('/users/register', methods=['POST'])
def user_reg():
    if not User.validator(request.form): #before we register, we need to validate the user
        return redirect('/login') # we redirect back to the homepage with the form
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form, 
        'password':hashed_pass
    }
    user_id = User.create(data)
    session['user_id'] = user_id
    return redirect("/home")

#look up a user by that email 
#check that user's password against the password provided 
@app.route('/users/login', methods=['POST'])
def user_log():
    data = {
        'email': request.form['email']
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Credentials", "log")
        return redirect('/login')
    if not bcrypt.check_password_hash(user_in_db.password,request.form['password']):
        flash("Invalid Credentials", "log")
        return redirect('/login')
    session['user_id'] = user_in_db.id #store the id of the user object
    return redirect('/home')

@app.route("/users/logout")
def log_out():
    del session['user_id']
    return redirect('/')

#Route to the Read Page
@app.route("/users/read")
def logged_in_read_page_route():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    logged_user = User.get_by_id(data)
    return render_template("read.html", logged_user=logged_user)

#Route to the Listen Page
@app.route("/users/listen")
def logged_in_listen_page_route():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    logged_user = User.get_by_id(data)
    return render_template("listen.html", logged_user=logged_user)

# --------- API ENDPOINT ROUTE -----------------------------------

# score | endpoint
@app.route("/score/{post_id}?scale=100", methods=['POST'])
def score_of_user_recording():
    pass 


