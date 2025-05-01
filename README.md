# Online Dairy Delivery System

A full-stack web application for managing dairy product deliveries online.

## Features

### Admin Features
- Admin login with validation
- Product management (add, edit, delete)
- Price management
- User management
- Sales reports and analytics

### User Features
- User registration and login
- Product browsing
- Shopping cart functionality
- Payment processing

## Tech Stack
- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
- Database: SQLite
- Authentication: Flask-Login

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Run the application:
```bash
flask run
```

The application will be available at `http://localhost:5000`

## Default Admin Credentials
- Email: admin@dairy.com
- Password: admin123

## Project Structure
```
dairy_delivery/
├── backend/
│   ├── models/
│   ├── routes/
│   ├── static/
│   └── templates/
├── frontend/
│   ├── css/
│   ├── js/
│   └── images/
├── instance/
├── migrations/
├── requirements.txt
└── README.md
``` 