from db import db
from models.cart import Cart
from models.menu import Menu
from sqlalchemy import and_

class CartDAO:
    def add_to_cart(self, user_id, menu_id, quantity=1):
        try:
            # Check if item already exists in cart
            existing_cart = Cart.query.filter(and_(
                Cart.user_id == user_id,
                Cart.menu_id == menu_id
            )).first()
            
            if existing_cart:
                existing_cart.quantity += quantity
                db.session.commit()
                return existing_cart
            else:
                cart = Cart(
                    user_id=user_id,
                    menu_id=menu_id,
                    quantity=quantity
                )
                db.session.add(cart)
                db.session.commit()
                return cart
        except Exception as e:
            db.session.rollback()
            print(f"Error adding to cart: {e}")
            return None
    
    def get_cart_items(self, user_id):
        return Cart.query.filter_by(user_id=user_id).join(Menu).all()
    
    def update_cart_quantity(self, user_id, cart_id, quantity):
        try:
            cart = Cart.query.filter(and_(
                Cart.id == cart_id,
                Cart.user_id == user_id
            )).first()
            
            if cart:
                cart.quantity = quantity
                db.session.commit()
                return cart
            return None
        except Exception as e:
            db.session.rollback()
            print(f"Error updating cart quantity: {e}")
            return None
    
    def remove_from_cart(self, user_id, cart_id):
        try:
            cart = Cart.query.filter(and_(
                Cart.id == cart_id,
                Cart.user_id == user_id
            )).first()
            
            if cart:
                db.session.delete(cart)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error removing from cart: {e}")
            return False
    
    def clear_cart(self, user_id):
        try:
            Cart.query.filter_by(user_id=user_id).delete()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error clearing cart: {e}")
            return False
    
    def get_cart_total(self, user_id):
        cart_items = self.get_cart_items(user_id)
        return sum(item.menu.price * item.quantity for item in cart_items)
    
    def get_cart_count(self, user_id):
        return Cart.query.filter_by(user_id=user_id).count()