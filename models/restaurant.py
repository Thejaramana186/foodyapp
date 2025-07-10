from db import db
from datetime import datetime

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cuisine = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, default=0.0)
    delivery_time = db.Column(db.String(20), nullable=True)
    image = db.Column(db.String(200), nullable=True)
    type = db.Column(db.String(20), nullable=False, default='both')  # 'veg', 'non-veg', 'both'
    address = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    menus = db.relationship('Menu', backref='restaurant', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cuisine': self.cuisine,
            'rating': self.rating,
            'delivery_time': self.delivery_time,
            'image': self.image,
            'type': self.type,
            'address': self.address,
            'phone': self.phone,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Restaurant {self.name}>'