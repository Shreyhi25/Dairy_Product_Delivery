from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from backend.models.models import Product, CartItem, Order, OrderItem
from backend.app import db

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/dashboard')
@login_required
def dashboard():
    products = Product.query.all()
    return render_template('user/dashboard.html', products=products)

@user_bp.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('user/cart.html', cart_items=cart_items, total=total)

@user_bp.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    if quantity > product.stock:
        flash('Not enough stock available')
        return redirect(url_for('user.dashboard'))
    
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Product added to cart')
    return redirect(url_for('user.cart'))

@user_bp.route('/cart/update/<int:cart_item_id>', methods=['POST'])
@login_required
def update_cart(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    
    if cart_item.user_id != current_user.id:
        flash('Unauthorized action')
        return redirect(url_for('user.cart'))
    
    quantity = int(request.form.get('quantity', 1))
    
    if quantity > cart_item.product.stock:
        flash('Not enough stock available')
        return redirect(url_for('user.cart'))
    
    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = quantity
    
    db.session.commit()
    return redirect(url_for('user.cart'))

@user_bp.route('/cart/remove/<int:cart_item_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    
    if cart_item.user_id != current_user.id:
        flash('Unauthorized action')
        return redirect(url_for('user.cart'))
    
    db.session.delete(cart_item)
    db.session.commit()
    
    flash('Item removed from cart')
    return redirect(url_for('user.cart'))

@user_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Your cart is empty')
        return redirect(url_for('user.cart'))
    
    if request.method == 'POST':
        # Create new order
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        order = Order(user_id=current_user.id, total_amount=total_amount)
        db.session.add(order)
        
        # Create order items and update stock
        for cart_item in cart_items:
            if cart_item.quantity > cart_item.product.stock:
                flash('Not enough stock available for some items')
                return redirect(url_for('user.cart'))
            
            order_item = OrderItem(
                order=order,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price_at_time=cart_item.product.price
            )
            db.session.add(order_item)
            
            # Update product stock
            cart_item.product.stock -= cart_item.quantity
            
            # Remove cart item
            db.session.delete(cart_item)
        
        db.session.commit()
        flash('Order placed successfully')
        return redirect(url_for('user.orders'))
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('user/checkout.html', cart_items=cart_items, total=total)

@user_bp.route('/orders')
@login_required
def orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('user/orders.html', orders=orders) 