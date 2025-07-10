from db import db
from models.restaurant import Restaurant
from sqlalchemy import or_

class RestaurantDAO:
    def create_restaurant(self, restaurant):
        try:
            db.session.add(restaurant)
            db.session.commit()
            return restaurant
        except Exception as e:
            db.session.rollback()
            print(f"Error creating restaurant: {e}")
            return None
    
    def get_restaurant_by_id(self, restaurant_id):
        return Restaurant.query.get(restaurant_id)
    
    def get_restaurants(self, page=1, per_page=10, search='', cuisine='', type_filter=''):
        query = Restaurant.query.filter_by(is_active=True)
        
        if search:
            query = query.filter(or_(
                Restaurant.name.ilike(f'%{search}%'),
                Restaurant.cuisine.ilike(f'%{search}%')
            ))
        
        if cuisine:
            query = query.filter_by(cuisine=cuisine)
        
        if type_filter:
            if type_filter == 'veg':
                query = query.filter(Restaurant.type.in_(['veg', 'both']))
            elif type_filter == 'non-veg':
                query = query.filter(Restaurant.type.in_(['non-veg', 'both']))
        
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    def get_all_cuisines(self):
        cuisines = db.session.query(Restaurant.cuisine).distinct().all()
        return [cuisine[0] for cuisine in cuisines]
    
    def update_restaurant(self, restaurant):
        try:
            db.session.commit()
            return restaurant
        except Exception as e:
            db.session.rollback()
            print(f"Error updating restaurant: {e}")
            return None
    
    def delete_restaurant(self, restaurant_id):
        try:
            restaurant = Restaurant.query.get(restaurant_id)
            if restaurant:
                restaurant.is_active = False
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting restaurant: {e}")
            return False
    
    def get_featured_restaurants(self, limit=6):
        return Restaurant.query.filter_by(is_active=True).order_by(Restaurant.rating.desc()).limit(limit).all()