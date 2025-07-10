from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from db import db
from models.user import User
from models.restaurant import Restaurant
from models.menu import Menu
from models.cart import Cart
from models.order import Order
from controllers.login_controller import login_bp
from controllers.register_controller import register_bp
from controllers.restaurant_controller import restaurant_bp
from controllers.menu_controller import menu_bp
from controllers.cart_controller import cart_bp
from controllers.checkout_controller import checkout_bp
from controllers.order_history_controller import order_history_bp
from controllers.logout_controller import logout_bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(checkout_bp)
    app.register_blueprint(order_history_bp)
    app.register_blueprint(logout_bp)
    
    @app.route('/')
    def index():
        featured_restaurants = Restaurant.query.filter_by(is_active=True).order_by(Restaurant.rating.desc()).limit(8).all()
        cuisines = db.session.query(Restaurant.cuisine).distinct().limit(8).all()
        return render_template('index.html', restaurants=featured_restaurants, cuisines=[c[0] for c in cuisines])
    
    @app.errorhandler(404)
    def not_found(error):
        return render_template('error.html', error="Page not found"), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('error.html', error="Internal server error"), 500
    
    with app.app_context():
        db.create_all()
        seed_data()
    
    return app

def seed_data():
    # Check if data already exists
    if Restaurant.query.count() > 0:
        return
    
    # Comprehensive Indian and Western menu items
    indian_menus = {
        'North Indian': [
            {'name': 'Butter Chicken', 'price': 16.99, 'description': 'Tender chicken in rich tomato-cream curry', 'category': 'Main Course', 'type': 'non-veg'},
            {'name': 'Paneer Butter Masala', 'price': 14.99, 'description': 'Cottage cheese in velvety tomato gravy', 'category': 'Main Course', 'type': 'veg'},
            {'name': 'Dal Makhani', 'price': 12.99, 'description': 'Creamy black lentils slow-cooked overnight', 'category': 'Main Course', 'type': 'veg'},
            {'name': 'Chicken Tikka Masala', 'price': 17.99, 'description': 'Grilled chicken in spiced tomato curry', 'category': 'Main Course', 'type': 'non-veg'},
            {'name': 'Palak Paneer', 'price': 13.99, 'description': 'Cottage cheese in fresh spinach gravy', 'category': 'Main Course', 'type': 'veg'},
            {'name': 'Rogan Josh', 'price': 19.99, 'description': 'Aromatic lamb curry with Kashmiri spices', 'category': 'Main Course', 'type': 'non-veg'},
            {'name': 'Chole Bhature', 'price': 11.99, 'description': 'Spiced chickpeas with fluffy bread', 'category': 'Main Course', 'type': 'veg'},
            {'name': 'Chicken Biryani', 'price': 18.99, 'description': 'Fragrant basmati rice with spiced chicken', 'category': 'Rice', 'type': 'non-veg'},
            {'name': 'Vegetable Biryani', 'price': 15.99, 'description': 'Aromatic rice with mixed vegetables', 'category': 'Rice', 'type': 'veg'},
            {'name': 'Butter Naan', 'price': 4.99, 'description': 'Soft leavened bread with butter', 'category': 'Bread', 'type': 'veg'},
            {'name': 'Garlic Naan', 'price': 5.99, 'description': 'Naan bread with fresh garlic and herbs', 'category': 'Bread', 'type': 'veg'},
            {'name': 'Tandoori Chicken', 'price': 16.99, 'description': 'Marinated chicken cooked in clay oven', 'category': 'Tandoor', 'type': 'non-veg'},
            {'name': 'Paneer Tikka', 'price': 14.99, 'description': 'Grilled cottage cheese with spices', 'category': 'Tandoor', 'type': 'veg'},
            {'name': 'Seekh Kebab', 'price': 15.99, 'description': 'Spiced minced meat skewers', 'category': 'Tandoor', 'type': 'non-veg'},
            {'name': 'Masala Chai', 'price': 3.99, 'description': 'Spiced Indian tea with milk', 'category': 'Beverage', 'type': 'veg'},
            {'name': 'Mango Lassi', 'price': 5.99, 'description': 'Refreshing mango yogurt drink', 'category': 'Beverage', 'type': 'veg'},
            {'name': 'Gulab Jamun', 'price': 6.99, 'description': 'Sweet milk dumplings in sugar syrup', 'category': 'Dessert', 'type': 'veg'},
            {'name': 'Kulfi', 'price': 5.99, 'description': 'Traditional Indian ice cream', 'category': 'Dessert', 'type': 'veg'}
        ],
        'South Indian': [
            {'name': 'Masala Dosa', 'price': 9.99, 'description': 'Crispy crepe with spiced potato filling', 'category': 'Main Course', 'type': 'veg'},
            {'name': 'Idli Sambar', 'price': 8.99, 'description': 'Steamed rice cakes with lentil curry', 'category': 'Main Course', 'type': 'veg'},
            {'name': 'Chicken Chettinad', 'price': 17.99, 'description': 'Spicy South Indian chicken curry', 'category': 'Main Course', 'type': 'non-veg'},
            {'name': 'Fish Curry', 'price': 18.99, 'description': 'Coconut-based fish curry', 'category': 'Main Course', 'type': 'non-veg'},
            {'name': 'Sambar Rice', 'price': 10.99, 'description': 'Rice with tangy lentil curry', 'category': 'Rice', 'type': 'veg'},
            {'name': 'Rasam', 'price': 6.99, 'description': 'Tangy tomato-tamarind soup', 'category': 'Soup', 'type': 'veg'},
            {'name': 'Uttapam', 'price': 8.99, 'description': 'Thick savory pancake with vegetables', 'category': 'Main Course', 'type': 'veg'},
            {'name': 'Vada', 'price': 6.99, 'description': 'Crispy lentil donuts', 'category': 'Snack', 'type': 'veg'},
            {'name': 'Coconut Chutney', 'price': 3.99, 'description': 'Fresh coconut condiment', 'category': 'Side', 'type': 'veg'},
            {'name': 'Filter Coffee', 'price': 4.99, 'description': 'Traditional South Indian coffee', 'category': 'Beverage', 'type': 'veg'}
        ]
    }
    
    western_menus = {
        'Italian': [
            {'name': 'Margherita Pizza', 'price': 14.99, 'description': 'Fresh mozzarella, tomato sauce, basil', 'category': 'Pizza', 'type': 'veg'},
            {'name': 'Pepperoni Pizza', 'price': 17.99, 'description': 'Classic pepperoni with mozzarella', 'category': 'Pizza', 'type': 'non-veg'},
            {'name': 'Quattro Stagioni', 'price': 19.99, 'description': 'Four seasons pizza with varied toppings', 'category': 'Pizza', 'type': 'non-veg'},
            {'name': 'Spaghetti Carbonara', 'price': 16.99, 'description': 'Creamy pasta with bacon and eggs', 'category': 'Pasta', 'type': 'non-veg'},
            {'name': 'Fettuccine Alfredo', 'price': 15.99, 'description': 'Rich creamy pasta with parmesan', 'category': 'Pasta', 'type': 'veg'},
            {'name': 'Lasagna Bolognese', 'price': 18.99, 'description': 'Layered pasta with meat sauce', 'category': 'Pasta', 'type': 'non-veg'},
            {'name': 'Chicken Parmigiana', 'price': 19.99, 'description': 'Breaded chicken with tomato sauce', 'category': 'Main Course', 'type': 'non-veg'},
            {'name': 'Caesar Salad', 'price': 10.99, 'description': 'Crisp romaine with caesar dressing', 'category': 'Salad', 'type': 'veg'},
            {'name': 'Caprese Salad', 'price': 12.99, 'description': 'Fresh mozzarella, tomatoes, basil', 'category': 'Salad', 'type': 'veg'},
            {'name': 'Tiramisu', 'price': 7.99, 'description': 'Classic Italian coffee dessert', 'category': 'Dessert', 'type': 'veg'},
            {'name': 'Gelato', 'price': 6.99, 'description': 'Italian ice cream', 'category': 'Dessert', 'type': 'veg'},
            {'name': 'Espresso', 'price': 3.99, 'description': 'Strong Italian coffee', 'category': 'Beverage', 'type': 'veg'}
        ],
        'American': [
            {'name': 'Classic Cheeseburger', 'price': 13.99, 'description': 'Beef patty with cheese, lettuce, tomato', 'category': 'Burger', 'type': 'non-veg'},
            {'name': 'BBQ Bacon Burger', 'price': 16.99, 'description': 'Beef with BBQ sauce and crispy bacon', 'category': 'Burger', 'type': 'non-veg'},
            {'name': 'Veggie Burger', 'price': 11.99, 'description': 'Plant-based patty with fresh vegetables', 'category': 'Burger', 'type': 'veg'},
            {'name': 'Buffalo Wings', 'price': 12.99, 'description': 'Spicy chicken wings with blue cheese', 'category': 'Appetizer', 'type': 'non-veg'},
            {'name': 'BBQ Ribs', 'price': 22.99, 'description': 'Slow-cooked ribs with BBQ sauce', 'category': 'Main Course', 'type': 'non-veg'},
            {'name': 'Grilled Chicken Breast', 'price': 18.99, 'description': 'Herb-marinated grilled chicken', 'category': 'Main Course', 'type': 'non-veg'},
            {'name': 'Fish and Chips', 'price': 16.99, 'description': 'Beer-battered fish with crispy fries', 'category': 'Main Course', 'type': 'non-veg'},
            {'name': 'Mac and Cheese', 'price': 10.99, 'description': 'Creamy macaroni with cheese sauce', 'category': 'Main Course', 'type': 'veg'},
            {'name': 'French Fries', 'price': 5.99, 'description': 'Crispy golden potato fries', 'category': 'Side', 'type': 'veg'},
            {'name': 'Onion Rings', 'price': 6.99, 'description': 'Crispy battered onion rings', 'category': 'Side', 'type': 'veg'},
            {'name': 'Chocolate Brownie', 'price': 6.99, 'description': 'Rich chocolate brownie with vanilla ice cream', 'category': 'Dessert', 'type': 'veg'},
            {'name': 'Apple Pie', 'price': 7.99, 'description': 'Classic American apple pie', 'category': 'Dessert', 'type': 'veg'},
            {'name': 'Milkshake', 'price': 5.99, 'description': 'Creamy vanilla milkshake', 'category': 'Beverage', 'type': 'veg'},
            {'name': 'Iced Tea', 'price': 3.99, 'description': 'Refreshing iced tea', 'category': 'Beverage', 'type': 'veg'}
        ],
        'Mexican': [
            {'name': 'Chicken Tacos', 'price': 11.99, 'description': 'Soft tacos with seasoned chicken', 'category': 'Main Course', 'type': 'non-veg'},
            {'name': 'Beef Burritos', 'price': 13.99, 'description': 'Large tortilla with spiced beef', 'category': 'Main Course', 'type': 'non-veg'},
            {'name': 'Vegetable Quesadilla', 'price': 9.99, 'description': 'Grilled tortilla with cheese and vegetables', 'category': 'Main Course', 'type': 'veg'},
            {'name': 'Chicken Enchiladas', 'price': 14.99, 'description': 'Rolled tortillas with chicken and sauce', 'category': 'Main Course', 'type': 'non-veg'},
            {'name': 'Guacamole', 'price': 6.99, 'description': 'Fresh avocado dip with tortilla chips', 'category': 'Appetizer', 'type': 'veg'},
            {'name': 'Nachos Supreme', 'price': 10.99, 'description': 'Loaded nachos with cheese and toppings', 'category': 'Appetizer', 'type': 'veg'},
            {'name': 'Mexican Rice', 'price': 4.99, 'description': 'Seasoned rice with tomatoes and spices', 'category': 'Side', 'type': 'veg'},
            {'name': 'Refried Beans', 'price': 4.99, 'description': 'Traditional Mexican beans', 'category': 'Side', 'type': 'veg'},
            {'name': 'Churros', 'price': 6.99, 'description': 'Fried pastry with cinnamon sugar', 'category': 'Dessert', 'type': 'veg'},
            {'name': 'Horchata', 'price': 4.99, 'description': 'Sweet rice cinnamon drink', 'category': 'Beverage', 'type': 'veg'}
        ]
    }
    
    # 50+ Restaurant data
    restaurants_data = [
        # Indian Restaurants
        {'name': 'Spice Palace', 'cuisine': 'North Indian', 'rating': 4.8, 'delivery_time': '30-45 min', 'type': 'both', 'menu_type': 'North Indian'},
        {'name': 'Tandoor Express', 'cuisine': 'North Indian', 'rating': 4.9, 'delivery_time': '35-50 min', 'type': 'both', 'menu_type': 'North Indian'},
        {'name': 'Saffron Garden', 'cuisine': 'North Indian', 'rating': 4.7, 'delivery_time': '40-55 min', 'type': 'veg', 'menu_type': 'North Indian'},
        {'name': 'Masala Junction', 'cuisine': 'North Indian', 'rating': 4.6, 'delivery_time': '35-50 min', 'type': 'both', 'menu_type': 'North Indian'},
        {'name': 'Curry Palace', 'cuisine': 'North Indian', 'rating': 4.8, 'delivery_time': '40-55 min', 'type': 'non-veg', 'menu_type': 'North Indian'},
        {'name': 'Punjabi Dhaba', 'cuisine': 'North Indian', 'rating': 4.7, 'delivery_time': '40-55 min', 'type': 'both', 'menu_type': 'North Indian'},
        {'name': 'Biryani House', 'cuisine': 'North Indian', 'rating': 4.9, 'delivery_time': '45-60 min', 'type': 'both', 'menu_type': 'North Indian'},
        {'name': 'Spicy Treats', 'cuisine': 'North Indian', 'rating': 4.6, 'delivery_time': '35-50 min', 'type': 'veg', 'menu_type': 'North Indian'},
        {'name': 'Mughlai Flavors', 'cuisine': 'North Indian', 'rating': 4.9, 'delivery_time': '45-60 min', 'type': 'non-veg', 'menu_type': 'North Indian'},
        {'name': 'Rajasthani Thali', 'cuisine': 'North Indian', 'rating': 4.7, 'delivery_time': '40-55 min', 'type': 'veg', 'menu_type': 'North Indian'},
        {'name': 'Curry Express', 'cuisine': 'North Indian', 'rating': 4.8, 'delivery_time': '35-50 min', 'type': 'both', 'menu_type': 'North Indian'},
        {'name': 'Naan Stop', 'cuisine': 'North Indian', 'rating': 4.6, 'delivery_time': '30-45 min', 'type': 'both', 'menu_type': 'North Indian'},
        {'name': 'Tandoori Nights', 'cuisine': 'North Indian', 'rating': 4.9, 'delivery_time': '40-55 min', 'type': 'non-veg', 'menu_type': 'North Indian'},
        
        # South Indian Restaurants
        {'name': 'Dosa Delight', 'cuisine': 'South Indian', 'rating': 4.8, 'delivery_time': '30-45 min', 'type': 'veg', 'menu_type': 'South Indian'},
        {'name': 'Tiffin Express', 'cuisine': 'South Indian', 'rating': 4.4, 'delivery_time': '25-35 min', 'type': 'both', 'menu_type': 'South Indian'},
        {'name': 'Coconut Grove', 'cuisine': 'South Indian', 'rating': 4.7, 'delivery_time': '35-50 min', 'type': 'both', 'menu_type': 'South Indian'},
        {'name': 'Madras Kitchen', 'cuisine': 'South Indian', 'rating': 4.6, 'delivery_time': '30-45 min', 'type': 'non-veg', 'menu_type': 'South Indian'},
        {'name': 'Filter Coffee House', 'cuisine': 'South Indian', 'rating': 4.5, 'delivery_time': '20-30 min', 'type': 'veg', 'menu_type': 'South Indian'},
        
        # Italian Restaurants
        {'name': 'Bella Italia', 'cuisine': 'Italian', 'rating': 4.7, 'delivery_time': '25-35 min', 'type': 'non-veg', 'menu_type': 'Italian'},
        {'name': 'Pizza Corner', 'cuisine': 'Italian', 'rating': 4.4, 'delivery_time': '25-35 min', 'type': 'non-veg', 'menu_type': 'Italian'},
        {'name': 'Pasta Paradise', 'cuisine': 'Italian', 'rating': 4.3, 'delivery_time': '30-40 min', 'type': 'veg', 'menu_type': 'Italian'},
        {'name': 'Cheesy Delights', 'cuisine': 'Italian', 'rating': 4.3, 'delivery_time': '25-35 min', 'type': 'veg', 'menu_type': 'Italian'},
        {'name': 'Risotto Republic', 'cuisine': 'Italian', 'rating': 4.5, 'delivery_time': '30-45 min', 'type': 'veg', 'menu_type': 'Italian'},
        {'name': 'Gelato Dreams', 'cuisine': 'Italian', 'rating': 4.8, 'delivery_time': '15-25 min', 'type': 'veg', 'menu_type': 'Italian'},
        {'name': 'Little Italy', 'cuisine': 'Italian', 'rating': 4.6, 'delivery_time': '30-45 min', 'type': 'non-veg', 'menu_type': 'Italian'},
        {'name': 'Mamma Mia', 'cuisine': 'Italian', 'rating': 4.7, 'delivery_time': '25-35 min', 'type': 'both', 'menu_type': 'Italian'},
        {'name': 'Napoli Nights', 'cuisine': 'Italian', 'rating': 4.5, 'delivery_time': '35-50 min', 'type': 'non-veg', 'menu_type': 'Italian'},
        
        # American Restaurants
        {'name': 'Burger Kingdom', 'cuisine': 'American', 'rating': 4.5, 'delivery_time': '15-25 min', 'type': 'non-veg', 'menu_type': 'American'},
        {'name': 'Grilled Express', 'cuisine': 'American', 'rating': 4.7, 'delivery_time': '20-30 min', 'type': 'non-veg', 'menu_type': 'American'},
        {'name': 'BBQ Nation', 'cuisine': 'American', 'rating': 4.6, 'delivery_time': '35-50 min', 'type': 'non-veg', 'menu_type': 'American'},
        {'name': 'Steak House', 'cuisine': 'American', 'rating': 4.8, 'delivery_time': '40-55 min', 'type': 'non-veg', 'menu_type': 'American'},
        {'name': 'Fried Chicken Hub', 'cuisine': 'American', 'rating': 4.5, 'delivery_time': '20-30 min', 'type': 'non-veg', 'menu_type': 'American'},
        {'name': 'Grill Master', 'cuisine': 'American', 'rating': 4.7, 'delivery_time': '30-45 min', 'type': 'non-veg', 'menu_type': 'American'},
        {'name': 'All American Diner', 'cuisine': 'American', 'rating': 4.4, 'delivery_time': '25-35 min', 'type': 'both', 'menu_type': 'American'},
        
        # Mexican Restaurants
        {'name': 'Taco Fiesta', 'cuisine': 'Mexican', 'rating': 4.6, 'delivery_time': '20-30 min', 'type': 'both', 'menu_type': 'Mexican'},
        {'name': 'El Sombrero', 'cuisine': 'Mexican', 'rating': 4.5, 'delivery_time': '25-35 min', 'type': 'non-veg', 'menu_type': 'Mexican'},
        {'name': 'Burrito Bowl', 'cuisine': 'Mexican', 'rating': 4.4, 'delivery_time': '20-30 min', 'type': 'both', 'menu_type': 'Mexican'},
        {'name': 'Aztec Kitchen', 'cuisine': 'Mexican', 'rating': 4.7, 'delivery_time': '30-45 min', 'type': 'non-veg', 'menu_type': 'Mexican'},
        
        # Continental/Mixed Restaurants
        {'name': 'Green Leaf Cafe', 'cuisine': 'Continental', 'rating': 4.5, 'delivery_time': '25-35 min', 'type': 'veg', 'menu_type': 'American'},
        {'name': 'Mediterranean Delight', 'cuisine': 'Mediterranean', 'rating': 4.5, 'delivery_time': '30-45 min', 'type': 'veg', 'menu_type': 'Italian'},
        {'name': 'Bread Basket', 'cuisine': 'Continental', 'rating': 4.4, 'delivery_time': '20-30 min', 'type': 'veg', 'menu_type': 'American'},
        {'name': 'Healthy Bites', 'cuisine': 'Continental', 'rating': 4.4, 'delivery_time': '20-30 min', 'type': 'veg', 'menu_type': 'American'},
        {'name': 'Café Mocha', 'cuisine': 'Continental', 'rating': 4.3, 'delivery_time': '15-25 min', 'type': 'veg', 'menu_type': 'American'},
        {'name': 'Sandwich Studio', 'cuisine': 'Continental', 'rating': 4.3, 'delivery_time': '15-25 min', 'type': 'veg', 'menu_type': 'American'},
        {'name': 'Salad Bar', 'cuisine': 'Continental', 'rating': 4.4, 'delivery_time': '10-20 min', 'type': 'veg', 'menu_type': 'American'},
        {'name': 'Smoothie Station', 'cuisine': 'Continental', 'rating': 4.6, 'delivery_time': '10-15 min', 'type': 'veg', 'menu_type': 'American'},
        {'name': 'Bakery Bliss', 'cuisine': 'Continental', 'rating': 4.6, 'delivery_time': '15-25 min', 'type': 'veg', 'menu_type': 'American'},
        {'name': 'Juice Junction', 'cuisine': 'Continental', 'rating': 4.3, 'delivery_time': '10-15 min', 'type': 'veg', 'menu_type': 'American'},
        {'name': 'Waffle House', 'cuisine': 'Continental', 'rating': 4.5, 'delivery_time': '20-30 min', 'type': 'veg', 'menu_type': 'American'},
        {'name': 'Crepe Corner', 'cuisine': 'French', 'rating': 4.4, 'delivery_time': '25-35 min', 'type': 'veg', 'menu_type': 'Italian'},
        {'name': 'Soup Kitchen', 'cuisine': 'Continental', 'rating': 4.3, 'delivery_time': '15-25 min', 'type': 'veg', 'menu_type': 'American'},
        {'name': 'Wrap It Up', 'cuisine': 'Continental', 'rating': 4.5, 'delivery_time': '15-25 min', 'type': 'both', 'menu_type': 'American'},
        {'name': 'Dessert Paradise', 'cuisine': 'Continental', 'rating': 4.7, 'delivery_time': '20-30 min', 'type': 'veg', 'menu_type': 'American'}
    ]
    
    # Restaurant images from Pexels
    restaurant_images = [
        'https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=300',
        'https://images.pexels.com/photos/1639557/pexels-photo-1639557.jpeg?auto=compress&cs=tinysrgb&w=300',
        'https://images.pexels.com/photos/1410235/pexels-photo-1410235.jpeg?auto=compress&cs=tinysrgb&w=300',
        'https://images.pexels.com/photos/1132047/pexels-photo-1132047.jpeg?auto=compress&cs=tinysrgb&w=300',
        'https://images.pexels.com/photos/958545/pexels-photo-958545.jpeg?auto=compress&cs=tinysrgb&w=300',
        'https://images.pexels.com/photos/262978/pexels-photo-262978.jpeg?auto=compress&cs=tinysrgb&w=300',
        'https://images.pexels.com/photos/776538/pexels-photo-776538.jpeg?auto=compress&cs=tinysrgb&w=300',
        'https://images.pexels.com/photos/1566837/pexels-photo-1566837.jpeg?auto=compress&cs=tinysrgb&w=300'
    ]
    
    # Create all restaurants
    for i, restaurant_data in enumerate(restaurants_data):
        restaurant = Restaurant(
            name=restaurant_data['name'],
            cuisine=restaurant_data['cuisine'],
            rating=restaurant_data['rating'],
            delivery_time=restaurant_data['delivery_time'],
            image=restaurant_images[i % len(restaurant_images)],
            type=restaurant_data['type']
        )
        db.session.add(restaurant)
        db.session.flush()
        
        # Add menu items based on menu type
        menu_type = restaurant_data['menu_type']
        if menu_type in indian_menus:
            menu_items = indian_menus[menu_type]
        elif menu_type in western_menus:
            menu_items = western_menus[menu_type]
        else:
            menu_items = western_menus['American']  # Default
        
        # Add menu items
        for menu_item in menu_items:
            # Filter menu items based on restaurant type
            if restaurant_data['type'] == 'veg' and menu_item['type'] == 'non-veg':
                continue
            elif restaurant_data['type'] == 'non-veg' and menu_item['type'] == 'veg':
                continue
            
            menu = Menu(
                restaurant_id=restaurant.id,
                name=menu_item['name'],
                price=menu_item['price'],
                description=menu_item['description'],
                category=menu_item['category'],
                type=menu_item['type']
            )
            db.session.add(menu)
    
    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)