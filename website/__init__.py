from flask import Flask
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'LONDONBRIDGE'

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Redirect to login page
    login_manager.init_app(app)

    from .views import views
    from .auth import auth, users

    @login_manager.user_loader
    def load_user(id):
        return users.get(int(id))

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
