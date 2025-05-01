from flask import Flask, redirect, url_for
from flask_login import current_user
from .config import config
from .models import db, login_manager

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Register blueprints
        from .routes import auth, user, admin
        app.register_blueprint(auth.bp)
        app.register_blueprint(user.bp)
        app.register_blueprint(admin.bp)
        
        # Root route
        @app.route('/')
        def index():
            if current_user.is_authenticated:
                if current_user.is_admin:
                    return redirect(url_for('admin.dashboard'))
                return redirect(url_for('user.dashboard'))
            return redirect(url_for('auth.login'))
        
        return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 