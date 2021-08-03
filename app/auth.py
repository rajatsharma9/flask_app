from flask import Blueprint, render_template, redirect, url_for, request, flash  # noqa
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from .models import User
from . import db
from app import sess

auth = Blueprint('auth', __name__)


@auth.route('/signUp', methods=['GET', 'POST'])
def signup():
    """Show signUP page."""
    if request.method == 'POST':
        fullname = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # if this returns a user, then the email already exists in database
        user = User.query.filter_by(email=email).first()

        # if a user is found, we want to redirect back to signup page so user can try again
        if user:
            flash('A user already exists with that email address.')
            return redirect(url_for('auth.login'))

        # create new user with the form data. Hash the password so plaintext version isn't saved.
        new_user_object = User(fullName=fullname, email=email, username=username, password=generate_password_hash(password))
        db.session.add(new_user_object)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('signUp.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Show the Login Page."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            sess["user"] = True
            login_user(user)
            flash('Login Successfully')
            return redirect(url_for("main.user_post", user_id=user.id))

        flash('Invalid username/password combination')
        return redirect(url_for('auth.login'))

    return render_template('logIn.html')


@auth.route('/logout')
def logout():
    """Logout the current user."""
    sess["user"] = False
    logout_user()
    return render_template("home.html")
