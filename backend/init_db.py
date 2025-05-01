import os
import sys

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app
from backend.models.models import User, db

def init_db():
    app = create_app()
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(email='admin@example.com').first()
        if not admin:
            admin = User(
                email='admin@example.com',
                name='Admin User',
                is_admin=True
            )
            admin.set_password('admin123')  # Change this password in production!
            db.session.add(admin)
            db.session.commit()
            print('Admin user created successfully!')
            print('Admin login credentials:')
            print('Email: admin@example.com')
            print('Password: admin123')
        else:
            print('Admin user already exists.')

if __name__ == '__main__':
    init_db() 