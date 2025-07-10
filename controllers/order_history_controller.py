from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from dao.order_dao import OrderDAO

order_history_bp = Blueprint('order_history', __name__)
order_dao = OrderDAO()

@order_history_bp.route('/order_history')
def order_history():
    if 'user_id' not in session:
        flash('Please login to view order history', 'error')
        return redirect(url_for('login.login'))
    
    user_id = session['user_id']
    page = request.args.get('page', 1, type=int)
    
    # Use safe method that handles database schema issues
    try:
        orders = order_dao.get_orders_by_user(user_id, page=page, per_page=10)
    except Exception as e:
        print(f"Error fetching orders: {e}")
        # Create empty pagination object
        from flask_sqlalchemy.pagination import Pagination

        orders = Pagination(None, page, 10, 0, [])
        flash('Unable to load order history. Please try again later.', 'error')
    
    return render_template('order_history.html', orders=orders)

@order_history_bp.route('/order/<int:order_id>')
def order_detail(order_id):
    if 'user_id' not in session:
        flash('Please login to view order details', 'error')
        return redirect(url_for('login.login'))
    
    user_id = session['user_id']
    order = order_dao.get_order_by_id(order_id)
    
    if not order or order.user_id != user_id:
        flash('Order not found', 'error')
        return redirect(url_for('order_history.order_history'))
    
    return render_template('order_detail.html', order=order)