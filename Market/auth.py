from flask import render_template , session , Blueprint , request , flash , redirect , url_for
from . import db
from .models import User
from flask_login import login_user , logout_user , login_required
from .models import User, is_valid_username, is_valid_email, is_valid_password

auth = Blueprint("auth",__name__)



@auth.route('/register', methods=["POST" , "GET"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')


        if not is_valid_email(email):
            flash("Invalid email format.", category='error')
            return render_template('register.html')

        if not is_valid_password(password1):
            flash("Password must be stronger(!@#A-Z&8)", category='error')
            return render_template('register.html')
        
        if not is_valid_username(username):
            flash("Invalid username format. Username must contain only letters and numbers.", category='error')
            return render_template('register.html')

        if password1 != password2:
            flash("Passwords do not match.", category='error')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash("Username already exists. Please choose a different username.", category='error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash("Email already exists.", category='error')

        new_user = User(email=email , username=username)
        new_user.set_password(password1)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful! You can now log in ", category="success")
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth.route('/login', methods=["POST" , "GET"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully', category='success')
            return redirect(url_for('home.home_page'))
        else:
            flash('Invalid email or password ', category='error')
            return render_template('login.html')

    return render_template("login.html")

@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out succsessfuly", category='success')
    return redirect(url_for('auth.login'))