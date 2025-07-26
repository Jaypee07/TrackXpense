from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import User
from app.forms import RegisterForm, LoginForm

main = Blueprint('main', __name__)

# Homepage route (visible to everyone)
@main.route('/')
def home():
    return render_template('home.html')  # Changed from base.html to home.html

# Register route
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account created. You can now log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

# Login route
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login failed. Check your email and password.', 'danger')
    return render_template('login.html', form=form)

# Dashboard route (only for logged-in users)
@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Logout route
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('main.login'))

# from flask import render_template, Blueprint
# from flask_login import login_required, current_user

# main = Blueprint('main', __name__)

# @main.route('/')
# def home():
#     return render_template('home.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
