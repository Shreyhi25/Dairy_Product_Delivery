from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from backend.models.models import User, Product, Order, OrderItem, CartItem
from backend.app import db
from datetime import datetime, timedelta
from sqlalchemy import func
from functools import wraps

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Access denied. Admin privileges required.')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_users = User.query.filter_by(is_admin=False).count()
    total_orders = Order.query.count()
    total_products = Product.query.count()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_orders=total_orders,
                         total_products=total_products,
                         recent_orders=recent_orders)

@bp.route('/products')
@login_required
@admin_required
def products():
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@bp.route('/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    if request.method == 'POST':
        product = Product(
            name=request.form['name'],
            description=request.form['description'],
            price=float(request.form['price']),
            stock=int(request.form['stock']),
            image_url=request.form['image_url']
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully')
        return redirect(url_for('admin.products'))
    return render_template('admin/add_product.html')

@bp.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.stock = int(request.form['stock'])
        product.image_url = request.form['image_url']
        db.session.commit()
        flash('Product updated successfully')
        return redirect(url_for('admin.products'))
    return render_template('admin/edit_product.html', product=product)

@bp.route('/products/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully')
    return redirect(url_for('admin.products'))

@bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.filter_by(is_admin=False).all()
    return render_template('admin/users.html', users=users)

@bp.route('/users/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.is_admin:
        flash('Cannot delete admin user')
        return redirect(url_for('admin.users'))
    
    # Delete associated orders and order items (cascade)
    Order.query.filter_by(user_id=user.id).delete()
    
    # Delete cart items
    CartItem.query.filter_by(user_id=user.id).delete()
    
    # Delete user
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully')
    return redirect(url_for('admin.users'))

@bp.route('/orders')
@login_required
@admin_required
def orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@bp.route('/reports')
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