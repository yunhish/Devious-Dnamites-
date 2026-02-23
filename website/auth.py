from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user
from .models import User


auth = Blueprint('auth', __name__)

# University email domain
UNIVERSITY_EMAIL_DOMAIN = '@wlv.ac.uk'

# Temporary in-memory storage for users (replace with database later)

users = {}
profiles = {}
user_id_counter = 1


def is_university_email(email):
    """Check if email is a valid university email"""
    return email.endswith(UNIVERSITY_EMAIL_DOMAIN)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    global user_id_counter
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if email is university email
        if not is_university_email(email):
            flash('Please use your university email address (@wlv.ac.uk).', category='error')
            return render_template("login.html")
        
        # Check if user exists
        user = None
        for u in users.values():
            if u.email == email:
                user = u
                break
        
        if user:
            # Create user session and log in
            login_user(user)
            flash('You have logged in successfully!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Email not found. Please sign up first.', category='error')
    
    return render_template("login.html")


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    global user_id_counter
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('fullName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Check if email is university email
        if not email or not is_university_email(email):
            flash('Please use your university email address (@wlv.ac.uk).', category='error')
        elif len(email) < 4:
           flash('Email must be greater than 3 characters.', category='error')  
        elif not first_name or len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif not password1 or not password2 or password1 != password2:
           flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Create new user and log them in
            new_user = User(user_id_counter, email, first_name)
            users[user_id_counter] = new_user
            # Create a profile for the new user
            from .models import Profile
            profiles[user_id_counter] = Profile(user_id_counter)
            user_id_counter += 1

            login_user(new_user)
            flash('Congratulations! Account and profile created successfully!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")
