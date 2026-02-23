from flask import Blueprint, render_template, request, redirect, url_for, flash

views = Blueprint('views', __name__)

@views.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

views = Blueprint('views', __name__)

user_settings = {}

@views.route('/settings', methods=['GET', 'POST'])
def settings():
    user = current_user
    if not user.is_authenticated:
        flash('You must be logged in to access settings.', 'error')
        return redirect(url_for('auth.login'))
    settings = user_settings.get(user.id, {'notifications': False, 'theme': 'light'})
    if request.method == 'POST':
        settings['notifications'] = bool(request.form.get('notifications'))
        settings['theme'] = request.form.get('theme', 'light')
        user_settings[user.id] = settings
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('views.settings'))
    return render_template('settings.html', settings=settings)

@views.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    user = current_user
    if not user.is_authenticated:
        flash('You must be logged in to edit your profile.', 'error')
        return redirect(url_for('auth.login'))
    profile = profiles.get(user.id)
    if request.method == 'POST':
        # Update user name
        new_name = request.form.get('first_name')
        if new_name:
            user.first_name = new_name
        # Update profile bio and avatar
        if profile:
            profile.bio = request.form.get('bio', profile.bio)
            profile.avatar_url = request.form.get('avatar_url', profile.avatar_url)
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('views.profile'))
    return render_template('edit_profile.html', user=user, profile=profile)

from flask import Blueprint, render_template, request
from flask_login import current_user
from .auth import profiles, users

views = Blueprint('views', __name__)

@views.route('/profile')
def profile():
    user = current_user
    profile = None
    if user.is_authenticated:
        profile = profiles.get(user.id)
    return render_template("profile.html", user=user, profile=profile)

@views.route('/search')
def search():
    query = request.args.get('q', '')
    # Placeholder: just echo the query for now
    return render_template('search.html', query=query)


@views.route('/')
def home():
    return render_template("home.html")


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

