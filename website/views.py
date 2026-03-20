from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from website.library_utils import is_library_open, get_library_services, get_busy_times

views = Blueprint('views', __name__)

# SU Events page
@views.route('/su-events')
def su_events():
    return render_template('su_events.html')

# Gym section subpages
@views.route('/gym/facilities')
def gym_facilities():
    return render_template('gym_facilities.html')

@views.route('/gym/membership')
def gym_membership():
    return render_template('gym_membership.html')

@views.route('/gym/hours')
def gym_hours():
    return render_template('gym_hours.html')

@views.route('/library')
def library():
    is_open = is_library_open()
    services = get_library_services()
    busy_times = get_busy_times()
    return render_template('library.html', is_open=is_open, services=services, busy_times=busy_times)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@views.route('/bus')
def bus():
    return render_template('bus.html')

@views.route('/gym')
def gym():
    return render_template('gym.html')

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
