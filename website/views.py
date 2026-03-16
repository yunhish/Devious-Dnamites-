from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@views.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        # Update user name
        current_user.first_name = request.form.get('first_name', current_user.first_name)
        
        # Update profile
        profile = current_user.profile
        profile.bio = request.form.get('bio', profile.bio)
        profile.avatar_url = request.form.get('avatar_url', profile.avatar_url)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('views.profile'))
    
    return render_template('edit_profile.html', user=current_user)

@views.route('/about')
def about():
    teams = [
        {"name": "Project Management Team", "members": ["Hisham champan yunusah"]},
        {"name": "Business Analysis Team", "members": ["Tyler McCallum", "Mandela Aina"]},
        {"name": "Data Analysis Team", "members": ["Benedict Zolana"]},
        {"name": "Software Development Team", "members": ["Mercy Ekuban", "Anu"]},
        {"name": "Security Consulting Team", "members": ["Lawrence kwame Anim"]},
    ]
    return render_template("about.html", teams=teams)

@views.route('/search')
def search():
    query = request.args.get('q', '')
    return render_template('search.html', query=query)

@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    # You can implement settings later
    return render_template("settings.html")

