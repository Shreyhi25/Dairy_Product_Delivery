from backend.app import create_app, db
from backend.models.models import User, Product
from werkzeug.security import generate_password_hash

def init_db():
    app = create_app()
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create admin user
        admin = User.query.filter_by(email='admin@dairy.com').first()
        if not admin:
            admin = User(
                email='admin@dairy.com',
                name='Admin User',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
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
        
        # Commit changes
        db.session.commit()
        print("Database initialized with sample data!")

if __name__ == '__main__':
    init_db() 