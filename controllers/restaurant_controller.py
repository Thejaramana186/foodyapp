from flask import Blueprint, request, render_template, jsonify
from models.restaurant import Restaurant
from dao.restaurant_dao import RestaurantDAO

restaurant_bp = Blueprint('restaurant', __name__)
restaurant_dao = RestaurantDAO()

@restaurant_bp.route('/restaurants')
def restaurants():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    cuisine = request.args.get('cuisine', '')
    type_filter = request.args.get('type', '')
    
    restaurants = restaurant_dao.get_restaurants(
        page=page,
        per_page=12,
        search=search,
        cuisine=cuisine,
        type_filter=type_filter
    )
    
    cuisines = restaurant_dao.get_all_cuisines()
    
    return render_template('restaurant_list.html', 
                         restaurants=restaurants, 
                         cuisines=cuisines,
                         search=search,
                         selected_cuisine=cuisine,
                         selected_type=type_filter)

@restaurant_bp.route('/restaurant/<int:restaurant_id>')
def restaurant_detail(restaurant_id):
    restaurant = restaurant_dao.get_restaurant_by_id(restaurant_id)
    if not restaurant:
        return render_template('error.html', error="Restaurant not found"), 404
    
    return render_template('restaurant_detail.html', restaurant=restaurant)