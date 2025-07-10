from db import db
from models.menu import Menu
from sqlalchemy import and_

class MenuDAO:
    def create_menu(self, menu):
        try:
            db.session.add(menu)
            db.session.commit()
            return menu
        except Exception as e:
            db.session.rollback()
            print(f"Error creating menu: {e}")
            return None
    
    def get_menu_by_id(self, menu_id):
        return Menu.query.get(menu_id)
    
    def get_menu_by_restaurant(self, restaurant_id, category='', type_filter=''):
        query = Menu.query.filter(and_(
            Menu.restaurant_id == restaurant_id,
            Menu.is_available == True
        ))
        
        if category:
            query = query.filter_by(category=category)
        
        if type_filter:
            query = query.filter_by(type=type_filter)
        
        return query.order_by(Menu.category, Menu.name).all()
    
    def get_categories_by_restaurant(self, restaurant_id):
        categories = db.session.query(Menu.category).filter(
            and_(Menu.restaurant_id == restaurant_id, Menu.is_available == True)
        ).distinct().all()
        return [category[0] for category in categories if category[0]]
    
    def update_menu(self, menu):
        try:
            db.session.commit()
            return menu
        except Exception as e:
            db.session.rollback()
            print(f"Error updating menu: {e}")
            return None
    
    def delete_menu(self, menu_id):
        try:
            menu = Menu.query.get(menu_id)
            if menu:
                menu.is_available = False
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting menu: {e}")
            return False
    
    def search_menu_items(self, search_term, page=1, per_page=10):
        query = Menu.query.filter(and_(
            Menu.name.ilike(f'%{search_term}%'),
            Menu.is_available == True
        ))
        
        return query.paginate(page=page, per_page=per_page, error_out=False)