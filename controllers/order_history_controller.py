from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from db import db
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
    
    print(f"Fetching order history for user ID: {user_id}")
    
    # Use safe method that handles database schema issues
    try:
        orders = order_dao.get_orders_by_user(user_id, page=page, per_page=10)
        print(f"Retrieved {orders.total} total orders, {len(orders.items)} on current page")
    except Exception as e:
        print(f"Error fetching orders: {e}")
        # Create simple empty pagination object
        class EmptyPagination:
            def __init__(self):
                self.items = []
                self.total = 0
                self.pages = 0
                self.page = page
                self.per_page = 10
                self.has_prev = False
                self.has_next = False
                self.prev_num = None
                self.next_num = None
            
            def iter_pages(self):
                return []
        
        orders = EmptyPagination()
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