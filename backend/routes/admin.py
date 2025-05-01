from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from backend.models.models import User, Product, Order, OrderItem, CartItem
from backend.app import db
from datetime import datetime, timedelta
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_users = User.query.filter_by(is_admin=False).count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_sales = db.session.query(func.sum(Order.total_amount)).filter(Order.status == 'completed').scalar() or 0
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_products=total_products,
                         total_orders=total_orders,
                         total_sales=total_sales)

@admin_bp.route('/products')
@login_required
@admin_required
def products():
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        image_url = request.form.get('image_url')
        
        product = Product(name=name, description=description, price=price,
                         stock=stock, image_url=image_url)
        
        db.session.add(product)
        db.session.commit()
        
        flash('Product added successfully')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/add_product.html')

@admin_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.stock = int(request.form.get('stock'))
        product.image_url = request.form.get('image_url')
        
        db.session.commit()
        flash('Product updated successfully')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/edit_product.html', product=product)

@admin_bp.route('/products/<int:product_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully')
    return redirect(url_for('admin.products'))

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.filter_by(is_admin=False).all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Don't allow deleting admin users
    if user.is_admin:
        flash('Cannot delete admin users')
        return redirect(url_for('admin.users'))
    
    # Delete user's orders and cart items first
    Order.query.filter_by(user_id=user_id).delete()
    CartItem.query.filter_by(user_id=user_id).delete()
    
    # Delete the user
    db.session.delete(user)
    db.session.commit()
    
    flash('User deleted successfully')
    return redirect(url_for('admin.users'))

@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    period = request.args.get('period', 'daily')
    
    if period == 'daily':
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=1)
    elif period == 'weekly':
        start_date = datetime.now().date() - timedelta(days=7)
        end_date = datetime.now().date() + timedelta(days=1)
    elif period == 'monthly':
        start_date = datetime.now().date() - timedelta(days=30)
        end_date = datetime.now().date() + timedelta(days=1)
    else:  # yearly
        start_date = datetime.now().date() - timedelta(days=365)
        end_date = datetime.now().date() + timedelta(days=1)
    
    orders = Order.query.filter(
        Order.created_at >= start_date,
        Order.created_at < end_date,
        Order.status == 'completed'
    ).all()
    
    total_sales = sum(order.total_amount for order in orders)
    
    return render_template('admin/reports.html',
                         period=period,
                         orders=orders,
                         total_sales=total_sales) 