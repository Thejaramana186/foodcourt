from flask import Blueprint, request, render_template, jsonify # import required modules from flask
from models.menu import Menu #import menu model
from models.restaurant import Restaurant #import restaurant model
from dao.menu_dao import MenuDAO #import menudao for database interaction

menu_bp = Blueprint('menu', __name__) #blueprint for menu related routes
menu_dao = MenuDAO() #instance for menudao to interact with the database

@menu_bp.route('/menu/<int:restaurant_id>') #route to display menuitems for aspecific restaurant
def menu(restaurant_id):
    #gets the restaurant by its id
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    #get filtered menuitems by category and type 
    category = request.args.get('category', '')
    type_filter = request.args.get('type', '')
    #get filtered menuitems from database
    menus = menu_dao.get_menu_by_restaurant(restaurant_id, category, type_filter)
    #get categories available in the restaurant menu
    categories = menu_dao.get_categories_by_restaurant(restaurant_id)
    #render the menu.html with all related data
    return render_template('menu.html',              # template to render,restaurant,filtered menu items ,available categories ,selected category,selected type filter
                         restaurant=restaurant,
                         menus=menus,
                         categories=categories,
                         selected_category=category,
                         selected_type=type_filter)



#route to return menuitem details as api
@menu_bp.route('/api/menu/<int:menu_id>')
def get_menu_item(menu_id):
    #get a menuitem by its id
    menu_item = menu_dao.get_menu_by_id(menu_id)
    #if the item exists
    if menu_item:
        return jsonify(menu_item.to_dict())
    return jsonify({'error': 'Menu item not found'}), 404   # if not found ..error response http 404