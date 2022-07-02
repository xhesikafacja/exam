from flask import render_template, redirect,session,request,flash
from flask_app import app

from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id']= id
    session['full_name']= request.form['first_name'] + ' ' + request.form['last_name']
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Yoo man this email is not registed yet! Wach u wanna do, hack me?!", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("You have forgotten your password again, havent you!", "login")
        return redirect('/')
    session['user_id'] = user.id
    session['full_name']= user.first_name + ' ' + user.last_name

    return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user_id']
    }
    return render_template("dashboard.html", user=User.get_by_id(data), recipes= Recipe.get_all())

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')
