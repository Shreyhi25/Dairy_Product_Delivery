# Dairy Product Delivery System

A modern e-commerce platform built with Flask for managing dairy product orders and deliveries.

## Description

The Dairy Product Delivery System is a comprehensive web application that facilitates online ordering and delivery management of dairy products. It features a robust admin panel for product and order management, along with a user-friendly interface for customers to browse products, manage their cart, and place orders.

## Key Features

### Admin Panel
- Product Management: Add, edit, and delete dairy products
- Order Management: View and process customer orders
- User Management: Monitor and manage user accounts
- Sales Analytics: Track sales performance and generate reports

### User Portal
- User Registration & Authentication
- Product Browsing & Search
- Shopping Cart Functionality
- Order History & Tracking
- Secure Checkout Process

### Order Processing
- Real-time Order Status Updates
- Automated Stock Management
- Order Confirmation & Notifications
- Delivery Tracking System

## Tech Stack

- **Frontend**
  - HTML5, CSS3, JavaScript
  - Bootstrap 5 for responsive design
  - Jinja2 templating engine

- **Backend**
  - Python 3.8+
  - Flask web framework
  - Flask-Login for authentication
  - SQLAlchemy ORM

- **Database**
  - MySQL for production
  - SQLite for development

## Installation

### Prerequisites
- Python 3.8 or higher
- MySQL Server (for production)
- pip package manager

### Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dairy_delivery.git
cd dairy_delivery
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure the database:
```bash
# For development (SQLite)
python backend/init_db.py

# For production (MySQL)
# Create a MySQL database named 'dairy_delivery'
# Update the DATABASE_URL in .env file
```

5. Set up environment variables:
Create a `.env` file in the root directory with:
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=mysql://username:password@localhost/dairy_delivery
```

6. Run the application:
```bash
python run.py
```

## Project Structure

```
dairy_delivery/
├── backend/
│   ├── models/         # Database models
│   ├── routes/         # Route handlers
│   ├── static/         # Static files
│   ├── templates/      # HTML templates
│   ├── app.py          # Flask application
│   ├── config.py       # Configuration
│   └── init_db.py      # Database initialization
├── requirements.txt    # Python dependencies
├── run.py             # Application entry point
└── .env               # Environment variables
```

## Usage

### Admin Access
- URL: `http://localhost:5000/admin`
- Default Admin Credentials:
  - Email: admin@example.com
  - Password: admin123

### User Access
- URL: `http://localhost:5000`
- Registration required for new users

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

For support, please:
- Open an issue in the GitHub repository
- Contact the maintainer at your-email@example.com

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Flask Documentation
- Bootstrap Documentation
- SQLAlchemy Documentation 