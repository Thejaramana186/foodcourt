from flask import Blueprint, request, render_template, jsonify  # import required modules from flask 
from models.restaurant import Restaurant #import the restaurant modle
from dao.restaurant_dao import RestaurantDAO # import the restaurantdao

restaurant_bp = Blueprint('restaurant', __name__) #blueprint for restaurant related routes
restaurant_dao = RestaurantDAO()# instance of the restaurantdao to interact with the database

@restaurant_bp.route('/restaurants') # route to display a paginated and filterable list of restaurant
def restaurants():
    #get the current page number
    page = request.args.get('page', 1, type=int)
    #get the search keyword from query parameter
    search = request.args.get('search', '')
    #get the selected cuisine type from query parameter
    cuisine = request.args.get('cuisine', '')
    #get the selected restaurant ---veg,non veg
    type_filter = request.args.get('type', '')
    

    #fetch filtered and paginated restaurant list from dao
    restaurants = restaurant_dao.get_restaurants(
        page=page,
        per_page=12,
        search=search,
        cuisine=cuisine,
        type_filter=type_filter
    )
    


    #get all the available cuisines 
    cuisines = restaurant_dao.get_all_cuisines()
    #render the restaurant list with the filtered data
    return render_template('restaurant_list.html', 
                         restaurants=restaurants,  # list of restaurants 
                         cuisines=cuisines, #list of all cuisine types
                         search=search, #search value to template
                         selected_cuisine=cuisine,  #currently selected cuisine 
                         selected_type=type_filter) # selected type of veg or nonveg


#route to display details of a specific restaurant id
@restaurant_bp.route('/restaurant/<int:restaurant_id>')
def restaurant_detail(restaurant_id):
    #fetch the restaurant details by id from databsase
    restaurant = restaurant_dao.get_restaurant_by_id(restaurant_id)
    #if no restaurant is found ,render an error page of 404
    if not restaurant:
        return render_template('error.html', error="Restaurant not found"), 404
    #if restaurant is found ,render the detail page 
    return render_template('restaurant_detail.html', restaurant=restaurant)