from db import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')  # 'pending', 'confirmed', 'preparing', 'delivered', 'cancelled'
    booking_name = db.Column(db.String(100), nullable=True)
    booking_email = db.Column(db.String(120), nullable=True)
    delivery_date = db.Column(db.Date, nullable=True)
    delivery_time = db.Column(db.String(20), nullable=True)
    delivery_address = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    payment_method = db.Column(db.String(50), nullable=True)
    special_instructions = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    restaurant = db.relationship('Restaurant', backref='orders', lazy=True)
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'restaurant_id': self.restaurant_id,
            'total_amount': self.total_amount,
            'status': self.status,
            'booking_name': self.booking_name,
            'booking_email': self.booking_email,
            'delivery_date': self.delivery_date.isoformat() if self.delivery_date else None,
            'delivery_time': self.delivery_time,
            'delivery_address': self.delivery_address,
            'phone': self.phone,
            'payment_method': self.payment_method,
            'special_instructions': self.special_instructions,
            'restaurant': self.restaurant.to_dict() if self.restaurant else None,
            'order_items': [item.to_dict() for item in self.order_items],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Order {self.id}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    # Relationships
    menu = db.relationship('Menu', backref='order_items', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'menu_id': self.menu_id,
            'quantity': self.quantity,
            'price': self.price,
            'menu': self.menu.to_dict() if self.menu else None
        }
    
    def __repr__(self):
        return f'<OrderItem {self.id}>'