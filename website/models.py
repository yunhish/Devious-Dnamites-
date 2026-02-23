from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, first_name):
        self.id = id
        self.email = email
        self.first_name = first_name

class Profile:
    def __init__(self, user_id, bio="", avatar_url=None):
        self.user_id = user_id
        self.bio = bio
        self.avatar_url = avatar_url
