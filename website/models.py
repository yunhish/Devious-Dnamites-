from flask_login import UserMixin
from . import db
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # ADDED THIS!
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150))  # ADDED THIS!
    student_id = db.Column(db.String(50), unique=True)  # ADDED THIS!
    points = db.Column(db.Integer, default=0)  # ADDED THIS!
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # ADDED THIS!

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    bio = db.Column(db.Text, default='')
    avatar_url = db.Column(db.String(500))
