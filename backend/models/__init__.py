"""
Database models package.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

from .models import User, Product, Order, OrderItem, CartItem 