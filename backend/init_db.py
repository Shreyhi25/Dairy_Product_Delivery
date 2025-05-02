import os
import sys

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app
from backend.models.models import User, Product, db

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
        
        # Create sample products
        sample_products = [
            {
                'name': 'Fresh Milk',
                'description': 'Pure and fresh milk from local farms',
                'price': 3.99,
                'stock': 100,
                'image_url': 'https://example.com/milk.jpg'
            },
            {
                'name': 'Cheddar Cheese',
                'description': 'Aged cheddar cheese, perfect for sandwiches',
                'price': 5.99,
                'stock': 50,
                'image_url': 'https://example.com/cheese.jpg'
            },
            {
                'name': 'Butter',
                'description': 'Creamy butter made from fresh cream',
                'price': 4.49,
                'stock': 75,
                'image_url': 'https://example.com/butter.jpg'
            },
            {
                'name': 'Yogurt',
                'description': 'Plain yogurt, great for breakfast or cooking',
                'price': 2.99,
                'stock': 60,
                'image_url': 'https://example.com/yogurt.jpg'
            },
            {
                'name': 'Cream',
                'description': 'Heavy cream for cooking and baking',
                'price': 3.49,
                'stock': 40,
                'image_url': 'https://example.com/cream.jpg'
            }
        ]
        
        for product_data in sample_products:
            product = Product.query.filter_by(name=product_data['name']).first()
            if not product:
                product = Product(**product_data)
                db.session.add(product)
        
        db.session.commit()
        print('Sample products created successfully!')

if __name__ == '__main__':
    init_db() 