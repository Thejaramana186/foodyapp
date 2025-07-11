from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from models.order import Order, OrderItem
from models.cart import Cart
from db import db
from dao.cart_dao import CartDAO
from dao.order_dao import OrderDAO
from datetime import datetime

checkout_bp = Blueprint('checkout', __name__)
cart_dao = CartDAO()
order_dao = OrderDAO()

@checkout_bp.route('/checkout')
def checkout():
    if 'user_id' not in session:
        flash('Please login to checkout', 'error')
        return redirect(url_for('login.login'))
    
    user_id = session['user_id']
    cart_items = cart_dao.get_cart_items(user_id)
    
    if not cart_items:
        flash('Your cart is empty', 'error')
        return redirect(url_for('cart.cart'))
    
    total = sum(item.menu.price * item.quantity for item in cart_items)
    
    return render_template('checkout.html', cart_items=cart_items, total=total)

@checkout_bp.route('/place_order', methods=['POST'])
def place_order():
    if 'user_id' not in session:
        flash('Please login to place order', 'error')
        return redirect(url_for('login.login'))
    
    user_id = session['user_id']
    booking_name = request.form.get('booking_name')
    booking_email = request.form.get('booking_email')
    delivery_date_str = request.form.get('delivery_date')
    delivery_time = request.form.get('delivery_time')
    delivery_address = request.form.get('delivery_address')
    phone = request.form.get('phone')
    payment_method = request.form.get('payment_method')
    special_instructions = request.form.get('special_instructions')
    
    # Convert delivery_date string to date object
    delivery_date = None
    if delivery_date_str:
        try:
            delivery_date = datetime.strptime(delivery_date_str, '%Y-%m-%d').date()
        except ValueError:
            pass
    
    if not all([booking_name, delivery_address, phone, payment_method]):
        flash('Please fill in all required fields', 'error')
        return redirect(url_for('checkout.checkout'))
    
    cart_items = cart_dao.get_cart_items(user_id)
    
    if not cart_items:
        flash('Your cart is empty', 'error')
        return redirect(url_for('cart.cart'))
    
    # Group items by restaurant
    restaurants_orders = {}
    for item in cart_items:
        restaurant_id = item.menu.restaurant_id
        if restaurant_id not in restaurants_orders:
            restaurants_orders[restaurant_id] = []
        restaurants_orders[restaurant_id].append(item)
    
    order_ids = []
    
    # Create separate orders for each restaurant
    for restaurant_id, items in restaurants_orders.items():
        total_amount = sum(item.menu.price * item.quantity for item in items)
        total_amount = total_amount * 1.05  # Add taxes
        
        # Create order
        order = Order(
            user_id=user_id,
            restaurant_id=restaurant_id,
            total_amount=total_amount,
            delivery_address=delivery_address,
            phone=phone,
            payment_method=payment_method,
            booking_name=booking_name,
            booking_email=booking_email,
            delivery_date=delivery_date,
            delivery_time=delivery_time,
            special_instructions=special_instructions
        )
        
        # Save order to database
        try:
            db.session.add(order)
            db.session.flush()  # Get the order ID
            order_id = order.id
            print(f"Created order with ID: {order_id}")
        except Exception as e:
            print(f"Error creating order: {e}")
            db.session.rollback()
            continue
        
        if order_id:
            order_ids.append(order_id)
            # Create order items
            for item in items:
                order_item = OrderItem(
                    order_id=order_id,
                    menu_id=item.menu_id,
                    quantity=item.quantity,
                    price=item.menu.price
                )
                try:
                    db.session.add(order_item)
                    print(f"Added order item: {item.menu.name} x {item.quantity}")
                except Exception as e:
                    print(f"Error creating order item: {e}")
    
    # Commit all changes
    try:
        db.session.commit()
        print(f"Successfully saved {len(order_ids)} orders")
    except Exception as e:
        print(f"Error committing orders: {e}")
        db.session.rollback()
        flash('Failed to place order. Please try again.', 'error')
        return redirect(url_for('checkout.checkout'))
    
    # Clear cart after successful order
    cart_dao.clear_cart(user_id)
    
    flash(f'Order placed successfully! Order ID(s): {", ".join(map(str, order_ids))}', 'success')
    return redirect(url_for('order_history.order_history'))