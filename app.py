# import necessary flask function and classes
from flask import Flask, render_template, request, redirect, url_for, session, flash 
#import config class
from config import Config
#import db database instance
from db import db
#import model classes which represents databse class
from models.user import User
from models.restaurant import Restaurant
from models.menu import Menu
from models.cart import Cart
from models.order import Order
#import blueprint routes from all the controllers
from controllers.login_controller import login_bp
from controllers.register_controller import register_bp
from controllers.restaurant_controller import restaurant_bp
from controllers.menu_controller import menu_bp
from controllers.cart_controller import cart_bp
from controllers.checkout_controller import checkout_bp
from controllers.order_history_controller import order_history_bp
from controllers.logout_controller import logout_bp
#import os 
import os
from db import db


def create_app():
    app = Flask(__name__) #create flask app instance 
    app.config.from_object(Config) #load config from config class
    
    # Initialize the  database with flask app
    db.init_app(app)
    
    # Register all the blueprints
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(checkout_bp)
    app.register_blueprint(order_history_bp)
    app.register_blueprint(logout_bp)
    

    #home page route 
    @app.route('/')
    def index():
        #fetch top restaurants filtered by highest rating 
        featured_restaurants = Restaurant.query.filter_by(is_active=True).order_by(Restaurant.rating.desc()).limit(8).all()
        #get distinct cuisines from the restaurant table
        cuisines = db.session.query(Restaurant.cuisine).distinct().limit(8).all()
        #render index.html
        return render_template('index.html', restaurants=featured_restaurants, cuisines=[c[0] for c in cuisines])
    
    #if any error ...error handler 404
    @app.errorhandler(404)
    def not_found(error):
        #show error.html with http status code 404
        return render_template('error.html', error="Page not found"), 404
    

    #error handler for 500
    @app.errorhandler(500)
    def internal_error(error):
        #show errorhtml page with http status code 500
        return render_template('error.html', error="Internal server error"), 500
    

    #create database table store data when the app starts
    with app.app_context():
        db.create_all() # create all the tables based on models
        seed_data() #insert sample data into the database
    
    return app #retrun flask app object 
#data seeding
def seed_data():
    # skip if there is already at least one restaurant
    if Restaurant.query.count() > 0:
        return
    
    # define sample menu data for indian and western cuisines
    indian_menus = {
        #north indian dishes
        'North Indian': [
            {'name': 'Butter Chicken', 'price': 300, 'description': ' Chicken cooked in a rich, buttery tomato gravy—creamy, savory, and comforting', 'category': 'Main Course', 'type': 'non-veg'},
            {'name': 'Mango Lassi', 'price': 80, 'description': 'Refreshing mango lassi', 'category': 'Beverage', 'type': 'veg'},
            {'name': 'Gulab Jamun', 'price': 120, 'description': 'Sweet gulab jamun', 'category': 'Dessert', 'type': 'veg'},
            {'name': 'Kulfi', 'price': 50, 'description': 'Indian ice cream', 'category': 'Dessert', 'type': 'veg'},
            {'name': 'Paneer Butter Masala', 'price': 250, 'description': 'Soft cottage cheese cubes simmered in creamy, tomato-based gravy—rich, mild, and flavorful', 'category': 'Main Course', 'type': 'veg'},
            {'name': 'Dal Makhani', 'price': 200, 'description': 'Slow-cooked black lentils in a creamy and buttery gravy—hearty, smooth, and comforting', 'category': 'Main Course', 'type': 'veg'},
            {'name': 'Chicken Tikka Masala', 'price': 350, 'description': 'Grilled chicken chunks served in a spiced tomato-cream sauce—smoky, tangy, and rich', 'category': 'Main Course', 'type': 'non-veg'},
            {'name': 'Palak Paneer', 'price': 240, 'description': 'Cottage cheese simmered in a silky spinach gravy—earthy, creamy, and nutritious', 'category': 'Main Course', 'type': 'veg'},
            {'name': 'Masala Chai', 'price': 3.99, 'description': 'Spiced Indian tea with milk', 'category': 'Beverage', 'type': 'veg'}
        ],
        #south indian dishes
        'South Indian': [
            {'name': 'Masala Dosa', 'price': 80, 'description': ' Thin, crispy rice pancake wrapped around a spiced potato filling—light, savory, and filling', 'category': 'Main Course', 'type': 'veg'},
            {'name': 'Idli Sambar', 'price': 40, 'description': 'Steamed rice cakes with lentil curry', 'category': 'Main Course', 'type': 'veg'},
            
            {'name': 'Uttapam', 'price': 70, 'description': 'Thick savory pancake with vegetables', 'category': 'Main Course', 'type': 'veg'},
            
            {'name': 'Coconut Chutney', 'price': 20, 'description': 'Smooth, mildly sweet coconut dip—perfect for dosa or idli', 'category': 'Side', 'type': 'veg'},
            {'name': 'Filter Coffee', 'price': 30, 'description': 'Strong, aromatic South Indian coffee with frothy milk—rich and energizing', 'category': 'Beverage', 'type': 'veg'},
            {'name': 'Chicken Chettinad', 'price': 200, 'description': 'Spicy South Indian chicken curry', 'category': 'Main Course', 'type': 'non-veg'},
            {'name': 'Fish Curry', 'price': 220, 'description': 'Coconut-based fish curry', 'category': 'Main Course', 'type': 'non-veg'},
            {'name': 'Sambar Rice', 'price': 60, 'description': 'Rice with tangy lentil curry', 'category': 'Rice', 'type': 'veg'},
            {'name': 'Rasam', 'price': 40, 'description': 'Tangy tomato-tamarind soup', 'category': 'Soup', 'type': 'veg'}
        ]
    }
    #western menu items
    western_menus = {
        #italian dishes
        'Italian': [
            {'name': 'Margherita Pizza', 'price': 180, 'description': 'Fresh mozzarella, tomato sauce, basil', 'category': 'Pizza', 'type': 'veg'},
            {'name': 'Pepperoni Pizza', 'price': 160, 'description': 'Classic pepperoni with mozzarella', 'category': 'Pizza', 'type': 'non-veg'},
            {'name': 'Quattro Stagioni', 'price': 220, 'description': 'Four seasons pizza with varied toppings', 'category': 'Pizza', 'type': 'non-veg'},
            
            {'name': 'Chicken Parmigiana', 'price': 180, 'description': 'Breaded chicken with tomato sauce', 'category': 'Main Course', 'type': 'non-veg'},
            {'name': 'Caesar Salad', 'price': 130, 'description': 'Crisp romaine with caesar dressing', 'category': 'Salad', 'type': 'veg'},
            {'name': 'Caprese Salad', 'price': 120, 'description': 'Fresh mozzarella, tomatoes, basil', 'category': 'Salad', 'type': 'veg'},
            {'name': 'Tiramisu', 'price':80, 'description': 'Classic Italian coffee dessert', 'category': 'Dessert', 'type': 'veg'},
            {'name': 'Gelato', 'price': 100, 'description': 'Italian ice cream', 'category': 'Dessert', 'type': 'veg'},
            {'name': 'Espresso', 'price': 70, 'description': 'Strong Italian coffee', 'category': 'Beverage', 'type': 'veg'},
            {'name': 'Spaghetti Carbonara', 'price': 190, 'description': 'Creamy pasta with bacon and eggs', 'category': 'Pasta', 'type': 'non-veg'},
            {'name': 'Fettuccine Alfredo', 'price': 150, 'description': 'Rich creamy pasta with parmesan', 'category': 'Pasta', 'type': 'veg'},
            {'name': 'Lasagna Bolognese', 'price': 200, 'description': 'Layered pasta with meat sauce', 'category': 'Pasta', 'type': 'non-veg'}



        ],
       
        #mexican dishes
        'Mexican': [
            {'name': 'Chicken Tacos', 'price': 200, 'description': 'Soft tacos with seasoned chicken', 'category': 'Main Course', 'type': 'non-veg'}, 
            {'name': 'Vegetable Quesadilla', 'price': 180, 'description': 'Grilled tortilla with cheese and vegetables', 'category': 'Main Course', 'type': 'veg'},
            {'name': 'Chicken Enchiladas', 'price': 190, 'description': 'Rolled tortillas with chicken and sauce', 'category': 'Main Course', 'type': 'non-veg'},
            {'name': 'Guacamole', 'price': 150, 'description': 'Fresh avocado dip with tortilla chips', 'category': 'Appetizer', 'type': 'veg'},
            
            {'name': 'Churros', 'price': 80, 'description': 'Fried pastry with cinnamon sugar', 'category': 'Dessert', 'type': 'veg'},
            {'name': 'Horchata', 'price': 90, 'description': 'Sweet rice cinnamon drink', 'category': 'Beverage', 'type': 'veg'}
        ]
    }
    
    # list of sample  50+ Restaurant data
    restaurants_data = [
        # Indian Restaurants
        {'name': 'Spice Palace', 'cuisine': 'North Indian', 'rating': 4.8, 'delivery_time': '30-45 min', 'type': 'both', 'menu_type': 'North Indian'},
        {'name': 'Tandoor Express', 'cuisine': 'North Indian', 'rating': 4.9, 'delivery_time': '35-50 min', 'type': 'both', 'menu_type': 'North Indian'},
        {'name': 'Saffron Garden', 'cuisine': 'North Indian', 'rating': 4.7, 'delivery_time': '40-55 min', 'type': 'veg', 'menu_type': 'North Indian'},
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
    
    # loop through each restaurant in data list
    for i, restaurant_data in enumerate(restaurants_data):
        #create restaurant object
        restaurant = Restaurant(
            name=restaurant_data['name'], #restaurant names
            cuisine=restaurant_data['cuisine'], #type of food
            rating=restaurant_data['rating'], #rating of the restaurant
            delivery_time=restaurant_data['delivery_time'], #delivery time
            image=restaurant_images[i % len(restaurant_images)], #cycle through images
            type=restaurant_data['type'] #veg ,non veg,or both
        )
        db.session.add(restaurant) #add to db 
        db.session.flush() #get the restaurant id before commit
        
        # determinebmenu type and select corresponding menu list
        menu_type = restaurant_data['menu_type']
        #get the restaurant menu type
        if menu_type in indian_menus:
            menu_items = indian_menus[menu_type]
            #pick items from indian menu list
        elif menu_type in western_menus:
            menu_items = western_menus[menu_type]
            #pick items from western menu list
        else:
            menu_items = western_menus['American'] 
            #if not found ,use american menu as default
        
        # loop through each menu item
        for menu_item in menu_items:
            # Filter menu items based on restaurant type
            if restaurant_data['type'] == 'veg' and menu_item['type'] == 'non-veg':
                continue
            elif restaurant_data['type'] == 'non-veg' and menu_item['type'] == 'veg':
                continue
            #create a menu item entry for the database
            menu = Menu(
                restaurant_id=restaurant.id,
                name=menu_item['name'],
                price=menu_item['price'],
                description=menu_item['description'],
                category=menu_item['category'],
                type=menu_item['type']
            )
            db.session.add(menu) #add menu item to the database session
    
    db.session.commit() # savae the commited changes to the database

#run the application 
if __name__ == '__main__':
    app = create_app() #create the app instance 
    app.run(debug=True) #run app in debug mode for development