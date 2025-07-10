from db import db
from models.order import Order, OrderItem
from models.restaurant import Restaurant
from sqlalchemy.orm import joinedload


class OrderDAO:
    def create_order(self, order):
        try:
            db.session.add(order)
            db.session.commit()
            return order.id
        except Exception as e:
            db.session.rollback()
            print(f"Error creating order: {e}")
            return None
    
    def create_order_item(self, order_item):
        try:
            db.session.add(order_item)
            db.session.commit()
            return order_item
        except Exception as e:
            db.session.rollback()
            print(f"Error creating order item: {e}")
            return None
    def get_order_by_id(self, order_id):
            return Order.query.options(
        joinedload(Order.order_items).joinedload(OrderItem.menu),
        joinedload(Order.restaurant)
    ).filter_by(id=order_id).first()

    
    def get_orders_by_user(self, user_id, page=1, per_page=10):
        try:
            return Order.query.options(
    joinedload(Order.order_items).joinedload(OrderItem.menu),
    joinedload(Order.restaurant)
).filter_by(user_id=user_id).order_by(Order.created_at.desc()).paginate(
    page=page, per_page=per_page, error_out=False
)

            
        except Exception as e:
            print(f"Error fetching orders: {e}")
            # Return empty pagination object
            from flask_sqlalchemy.pagination import Pagination

            class DummyPagination:
                def __init__(self, items, page, per_page):
                    self.items = items
        self.page = page
        self.per_page = per_page
        self.total = 0
        self.pages = 0
        return DummyPagination([], page, per_page)

    def get_orders_by_user_safe(self, user_id, page=1, per_page=10):
        """Safe method that handles missing columns gracefully"""
        try:
            # Try to get orders with all fields
            return Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).paginate(
                page=page, per_page=per_page, error_out=False
            )
        except Exception as e:
            print(f"Error with full order query: {e}")
            # Fallback to basic query without new fields
            from sqlalchemy import text
            try:
                result = db.session.execute(
                    text("SELECT id, user_id, restaurant_id, total_amount, status, delivery_address, phone, payment_method, created_at FROM orders WHERE user_id = :user_id ORDER BY created_at DESC LIMIT :limit OFFSET :offset"),
                    {'user_id': user_id, 'limit': per_page, 'offset': (page-1) * per_page}
                )
                orders = result.fetchall()
                total = db.session.execute(text("SELECT COUNT(*) FROM orders WHERE user_id = :user_id"), {'user_id': user_id}).scalar()
                
                # Convert to pagination-like object
                from flask_sqlalchemy import Pagination
                return Pagination(None, page, per_page, total, orders)
            except Exception as e2:
                print(f"Fallback query also failed: {e2}")
                from flask_sqlalchemy import Pagination
                return Pagination(None, page, per_page, 0, [])
            page=page, per_page=per_page, error_out=False
        
    
    def get_orders_by_restaurant(self, restaurant_id, page=1, per_page=10):
        return Order.query.filter_by(restaurant_id=restaurant_id).order_by(Order.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
    
    def update_order_status(self, order_id, status):
        try:
            order = Order.query.get(order_id)
            if order:
                order.status = status
                db.session.commit()
                return order
            return None
        except Exception as e:
            db.session.rollback()
            print(f"Error updating order status: {e}")
            return None
    
    def get_all_orders(self, page=1, per_page=10):
        return Order.query.order_by(Order.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
    
    def get_order_statistics(self, user_id=None, restaurant_id=None):
        query = Order.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        if restaurant_id:
            query = query.filter_by(restaurant_id=restaurant_id)
        
        total_orders = query.count()
        total_amount = db.session.query(db.func.sum(Order.total_amount)).filter(
            Order.user_id == user_id if user_id else True,
            Order.restaurant_id == restaurant_id if restaurant_id else True
        ).scalar() or 0
        
        return {
            'total_orders': total_orders,
            'total_amount': total_amount
        }