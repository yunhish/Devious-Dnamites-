from flask import Blueprint, current_app, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from website.library_utils import is_library_open, get_library_services, get_busy_times

views = Blueprint('views', __name__)

def get_searchable_content():
    """Get all searchable content from the application."""
    content = []
    
    # Library content
    for service in get_library_services():
        content.append({
            'title': service,
            'category': 'Library Services',
            'url': '/library',
            'description': f'Library service: {service}'
        })
    
    # Gym content
    gym_items = [
        {'title': 'Gym Floor', 'description': 'Cardiovascular and strength training equipment', 'url': '/gym'},
        {'title': 'Swimming Pool', 'description': 'Indoor Olympic-size pool with lanes', 'url': '/gym'},
        {'title': 'Fitness Classes', 'description': 'Group fitness classes including yoga, spin, and aerobics', 'url': '/gym'},
        {'title': 'Personal Training', 'description': 'One-on-one training sessions with certified trainers', 'url': '/gym'},
        {'title': 'Sauna', 'description': 'Steam room and sauna facilities', 'url': '/gym'},
        {'title': 'Squash Courts', 'description': 'Professional squash courts available for booking', 'url': '/gym'},
        {'title': 'Sports Hall', 'description': 'Multi-purpose sports hall for basketball, badminton, and more', 'url': '/gym'},
        {'title': 'Membership', 'description': 'View membership plans and pricing', 'url': '/gym/membership'},
        {'title': 'Gym Hours', 'description': 'Opening hours and facility schedules', 'url': '/gym/hours'},
    ]
    for item in gym_items:
        content.append({
            'title': item['title'],
            'category': 'Gym & Sports',
            'url': item['url'],
            'description': item['description']
        })
    
    # Bus content
    bus_items = [
        {'title': 'Route A', 'description': 'City Campus ↔ Walsall Campus'},
        {'title': 'Route B', 'description': 'City Campus ↔ Telford Campus'},
        {'title': 'Route C', 'description': 'Walsall Campus ↔ Telford Campus'},
        {'title': 'City Campus Stop', 'description': 'Main departure point at Wulfruna Street'},
        {'title': 'Walsall Campus Stop', 'description': 'Stop at Walsall Campus'},
        {'title': 'Telford Campus Stop', 'description': 'Stop at Telford Campus'},
        {'title': 'Bus Times', 'description': 'Live bus times and schedules'},
        {'title': 'Campus Bus', 'description': 'Inter-campus shuttle service'},
    ]
    for item in bus_items:
        content.append({
            'title': item['title'],
            'category': 'Campus Bus',
            'url': '/bus',
            'description': item['description']
        })
    
    # Campus locations and facilities
    location_items = [
        {'title': 'Library', 'description': 'Main university library with study rooms and resources'},
        {'title': 'Student Union', 'description': 'Student center with events and facilities'},
        {'title': 'Dining Hall', 'description': 'Main cafeteria and food services'},
        {'title': 'Accommodation', 'description': 'Student housing and dormitories'},
        {'title': 'IT Support', 'description': 'Technology and IT support services'},
        {'title': 'Health Centre', 'description': 'University health and medical services'},
        {'title': 'Learning Centre', 'description': 'Academic support and tutoring'},
    ]
    for item in location_items:
        content.append({
            'title': item['title'],
            'category': 'Campus Locations',
            'url': '/dashboard',
            'description': item['description']
        })
    
    # Events and Activities
    event_items = [
        {'title': 'Student Events', 'description': 'Upcoming SU events and activities'},
        {'title': 'Clubs', 'description': 'Student clubs and societies'},
        {'title': 'Workshops', 'description': 'Educational workshops and seminars'},
    ]
    for item in event_items:
        content.append({
            'title': item['title'],
            'category': 'Events & Activities',
            'url': '/su-events',
            'description': item['description']
        })
    
    return content

def perform_search(query):
    """Search through all application content."""
    if not query or query.strip() == '':
        return []
    
    query_lower = query.lower()
    content = get_searchable_content()
    results = []
    
    for item in content:
        # Search in title
        if query_lower in item['title'].lower():
            results.append({**item, 'match_type': 'title'})
        # Search in description
        elif query_lower in item['description'].lower():
            results.append({**item, 'match_type': 'description'})
    
    # Sort results: title matches first, then by category
    results.sort(key=lambda x: (x['match_type'] != 'title', x['category'], x['title']))
    
    return results

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

@views.route('/rewards')
def rewards():
    return render_template('rewards.html')

@views.route('/ar-map')
def ar_map():
    return render_template('ar_map.html')

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
        {"name": "Business Analysis Team", "members": ["Tyler McCallum"]},
        {"name": "Data Analysis Team", "members": ["Mandela Aina", "Benedict Zolana"]},
        {"name": "Software Development Team", "members": ["Mercy Ekuban", "Anu"]},
        {"name": "Security Consulting Team", "members": ["Lawrence kwame Anim"]},
    ]
    return render_template("about.html", teams=teams)

@views.route('/search')
def search():
    query = request.args.get('q', '').strip()
    results = perform_search(query) if query else []
    return render_template('search.html', query=query, results=results, result_count=len(results))

@views.route('/enquiry', methods=['GET', 'POST'])
def enquiry():
    if request.method == 'POST':
        flash('Enquiry submitted successfully! We will get back to you within 2 working days.', 'success')
        return redirect(url_for('views.enquiry'))
    return render_template('enquiry.html')

@views.route('/map')
def campus_map():
    return render_template('map.html')

@views.route('/notifications')
def notifications():
    return render_template('notifications.html')

@views.route('/bus')
def bus():
    return render_template('bus.html')

@views.route('/gym')
def gym():
    return render_template('gym.html')

@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    # You can implement settings later
    return render_template("settings.html")
