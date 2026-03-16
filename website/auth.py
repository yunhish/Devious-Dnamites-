from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from .models import User, Profile
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
        user = User.query.filter_by(email=email).first()
        
        if user:
            # For now, we're not checking password - you can add this later
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('views.home'))
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
        first_name = request.form.get('fullName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Check if email is university email
        if not email or not is_university_email(email):
            flash('Please use your university email address (@wlv.ac.uk).', 'error')
        elif User.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', 'error')  
        elif not first_name or len(first_name) < 2:
            flash('First name must be greater than 1 character.', 'error')
        elif not password1 or not password2 or password1 != password2:
            flash('Passwords don\'t match.', 'error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', 'error')
        else:
            # Create new user (without password for now)
            new_user = User(email=email, first_name=first_name)
            
            # Add user to database
            db.session.add(new_user)
            db.session.flush()  # This gets the user ID
            
            # Create a profile for the new user
            new_profile = Profile(user_id=new_user.id)
            db.session.add(new_profile)
            
            # Commit both user and profile to database
            db.session.commit()

            # Log the user in
            login_user(new_user)
            flash('Congratulations! Account and profile created successfully!', 'success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")
