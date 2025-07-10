from flask import Blueprint, request, render_template, jsonify
from models.menu import Menu
from models.restaurant import Restaurant
from dao.menu_dao import MenuDAO

menu_bp = Blueprint('menu', __name__)
menu_dao = MenuDAO()

@menu_bp.route('/menu/<int:restaurant_id>')
def menu(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    
    category = request.args.get('category', '')
    type_filter = request.args.get('type', '')
    
    menus = menu_dao.get_menu_by_restaurant(restaurant_id, category, type_filter)
    categories = menu_dao.get_categories_by_restaurant(restaurant_id)
    
    return render_template('menu.html', 
                         restaurant=restaurant,
                         menus=menus,
                         categories=categories,
                         selected_category=category,
                         selected_type=type_filter)

@menu_bp.route('/api/menu/<int:menu_id>')
def get_menu_item(menu_id):
    menu_item = menu_dao.get_menu_by_id(menu_id)
    if menu_item:
        return jsonify(menu_item.to_dict())
    return jsonify({'error': 'Menu item not found'}), 404