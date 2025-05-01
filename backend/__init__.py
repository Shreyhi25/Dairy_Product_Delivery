"""
Dairy Delivery System backend package.
""" 

from flask import Flask
from .config import Config
from .models import db
from flask_login import LoginManager

def create_app():
    app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
    app.config.from_object(Config)
    
    db.init_app(app)
    # Initialize other extensions like LoginManager etc.
    
    from .routes.auth import auth_bp
    from .routes.admin import admin_bp
    from .routes.user import user_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp, url_prefix='/user')

    return app
