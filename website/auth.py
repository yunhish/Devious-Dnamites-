from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from . import db

auth = Blueprint('auth', __name__)
UNIVERSITY_EMAIL_DOMAIN = '@wlv.ac.uk'

def is_university_email(email):
    """Check if email is a valid university email"""
    return email.endswith(UNIVERSITY_EMAIL_DOMAIN)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if email is university email
        if not is_university_email(email):
            flash('Please use your university email address (@wlv.ac.uk).', 'error')
            return render_template("login.html")
        
        # Check if user exists
        from .models import User
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Check password
            if check_password_hash(user.password_hash, password):
                login_user(user)
                flash('Logged in successfully!', 'success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', 'error')
        else:
            flash('Email not found. Please sign up first.', 'error')
    
    return render_template("login.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')  # Fixed field name
        password = request.form.get('password')  # Simplified to single password field

        # Check if email is university email
        if not email or not is_university_email(email):
            flash('Please use your university email address (@wlv.ac.uk).', 'error')
        else:
            from .models import User
            if User.query.filter_by(email=email).first():
                flash('Email already exists.', 'error')
            elif len(email) < 4:
                flash('Email must be greater than 3 characters.', 'error')  
            elif not first_name or len(first_name) < 2:
                flash('First name must be greater than 1 character.', 'error')
            elif not password or len(password) < 7:
                flash('Password must be at least 7 characters.', 'error')
            else:
                # Create new user WITH PASSWORD HASH
                password_hash = generate_password_hash(password, method='pbkdf2:sha256')
                new_user = User(
                    email=email, 
                    first_name=first_name,
                    password_hash=password_hash,
                    points=0  # Default points
                )
                # Add user to database
                db.session.add(new_user)
                db.session.commit()
                # Log the user in
                login_user(new_user)
                flash('Account created successfully!', 'success')
                return redirect(url_for('views.home'))

    return render_template("sign_up.html")ss