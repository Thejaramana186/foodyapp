from flask import Blueprint, request, render_template, redirect, url_for, session, flash, jsonify
from models.cart import Cart
from models.menu import Menu
from dao.cart_dao import CartDAO

cart_bp = Blueprint('cart', __name__)
cart_dao = CartDAO()

@cart_bp.route('/cart')
def cart():
    if 'user_id' not in session:
        flash('Please login to view your cart', 'error')
        return redirect(url_for('login.login'))
    
    user_id = session['user_id']
    cart_items = cart_dao.get_cart_items(user_id)
    
    total = sum(item.menu.price * item.quantity for item in cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@cart_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401
    
    user_id = session['user_id']
    menu_id = request.json.get('menu_id')
    quantity = request.json.get('quantity', 1)
    
    if not menu_id:
        return jsonify({'error': 'Menu ID is required'}), 400
    
    # Check if menu item exists
    menu_item = Menu.query.get(menu_id)
    if not menu_item:
        return jsonify({'error': 'Menu item not found'}), 404
    
    # Add to cart
    cart_item = cart_dao.add_to_cart(user_id, menu_id, quantity)
    
    if cart_item:
        return jsonify({'message': 'Item added to cart successfully', 'cart_item': cart_item.to_dict()})
    else:
        return jsonify({'error': 'Failed to add item to cart'}), 500

@cart_bp.route('/update_cart', methods=['POST'])
def update_cart():
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401
    
    user_id = session['user_id']
    cart_id = request.json.get('cart_id')
    quantity = request.json.get('quantity')
    
    if not cart_id or quantity is None:
        return jsonify({'error': 'Cart ID and quantity are required'}), 400
    
    if quantity <= 0:
        # Remove item from cart
        if cart_dao.remove_from_cart(user_id, cart_id):
            return jsonify({'message': 'Item removed from cart'})
        else:
            return jsonify({'error': 'Failed to remove item from cart'}), 500
    else:
        # Update quantity
        cart_item = cart_dao.update_cart_quantity(user_id, cart_id, quantity)
        if cart_item:
            return jsonify({'message': 'Cart updated successfully', 'cart_item': cart_item.to_dict()})
        else:
            return jsonify({'error': 'Failed to update cart'}), 500

@cart_bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401
    
    user_id = session['user_id']
    cart_id = request.json.get('cart_id')
    
    if not cart_id:
        return jsonify({'error': 'Cart ID is required'}), 400
    
    if cart_dao.remove_from_cart(user_id, cart_id):
        return jsonify({'message': 'Item removed from cart successfully'})
    else:
        return jsonify({'error': 'Failed to remove item from cart'}), 500

@cart_bp.route('/clear_cart', methods=['POST'])
def clear_cart():
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401
    
    user_id = session['user_id']
    
    if cart_dao.clear_cart(user_id):
        return jsonify({'message': 'Cart cleared successfully'})
    else:
        return jsonify({'error': 'Failed to clear cart'}), 500