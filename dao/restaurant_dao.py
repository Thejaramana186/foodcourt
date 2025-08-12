from db import db #import db from db.py
from models.restaurant import Restaurant # import restaurant model
from sqlalchemy import or_ # import or_ to use in database queries...  it is for complex filtering 

class RestaurantDAO:   # define dao for restaurant model
    def create_restaurant(self, restaurant): # create new restaurant and saves it into the database
        try:
            db.session.add(restaurant)  # add new restaurant object 
            db.session.commit() # commit changes to the database
            return restaurant # return the created restaurant 
        except Exception as e:
            db.session.rollback() # if any exception occurs rollback 
            print(f"Error creating restaurant: {e}") # it show a message if any error occurs
            return None # return none on failure
    
    def get_restaurant_by_id(self, restaurant_id): # get's a restaurant by restaurant_id
        return Restaurant.query.get(restaurant_id)
    
    def get_restaurants(self, page=1, per_page=10, search='', cuisine='', type_filter=''): #get's a restaurant by filtering  such as cuisine type,type---veg/non-veg type
        query = Restaurant.query.filter_by(is_active=True)
        
        # search on name or cuisine 
        if search:
            query = query.filter(or_(
                Restaurant.name.ilike(f'%{search}%'),
                Restaurant.cuisine.ilike(f'%{search}%')
            ))
        # filter by cuisine type
        if cuisine:
            query = query.filter_by(cuisine=cuisine)
        
        #filter by food name in that veg/non-veg,both
        if type_filter:
            if type_filter == 'veg':
                query = query.filter(Restaurant.type.in_(['veg', 'both']))
            elif type_filter == 'non-veg':
                query = query.filter(Restaurant.type.in_(['non-veg', 'both']))
        
        return query.paginate(page=page, per_page=per_page, error_out=False) # returns paginated result
    
    def get_all_cuisines(self): #get unique cuisine types from all restaurants
        cuisines = db.session.query(Restaurant.cuisine).distinct().all() #cuisine names
        return [cuisine[0] for cuisine in cuisines]# return cuisine name from each result
    
    def update_restaurant(self, restaurant): # update an existing restaurant
        try:
            db.session.commit() # commit changes if any to database
            return restaurant #return updated object 
        except Exception as e:
            db.session.rollback() # if any exception occurs rollback 
            print(f"Error updating restaurant: {e}")#it shows error message 
            return None #return none on failure
    
    #mark the restaurant as inactive instead of deleting it
    def delete_restaurant(self, restaurant_id):
        try:
            restaurant = Restaurant.query.get(restaurant_id) #find restaurant by id
            if restaurant:
                restaurant.is_active = False # make inactive instead deleting 
                db.session.commit() # commit changes 
                return True# return true if it is inactived successfully
            return False # if not return failure 
        except Exception as e:
            db.session.rollback() # if any exception occurs rollback to error
            print(f"Error deleting restaurant: {e}") # print the error message 
            return False # deletion failed
    
    def get_featured_restaurants(self, limit=6): # gives top rated restaurants 
        return Restaurant.query.filter_by(is_active=True).order_by(Restaurant.rating.desc()).limit(limit).all() # return's according to the rating specified 