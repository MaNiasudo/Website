from flask import render_template , session , Blueprint , request , flash , redirect , url_for
from . import db
from .models import User

auth = Blueprint("auth",__name__)



@auth.route('/register', methods=["POST" , "GET"])
def register():
    if request.method == "POST":
        email = request.form('email')
        password1 = request.form('password1')
        password2 = request.form('password2')
        first_name = request.form('first_name')


        if password1 != password2:
            flash("Passwords do not match", category='error')
            render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash("Username already exists.", category='error')

        new_user = User(email=email , first_name=first_name)
        new_user.set_password(password1)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful! You can now log in ", category="success")
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')
@auth.route('/login')
def login():
    return render_template("login.html")