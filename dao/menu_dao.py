from db import db # import db from db.py
from models.menu import Menu #import menu model
from sqlalchemy import and_ #import sqlalchemy's

class MenuDAO: #defines data access object for menu
    def create_menu(self, menu):# create and add new menuitem to the database
        try:
            db.session.add(menu) # add the menuitems to the session 
            db.session.commit() #commit the changes 
            return menu # return the menu object if successful
        except Exception as e:
            db.session.rollback() # if any error occurs rollback
            print(f"Error creating menu: {e}") #print the error for debugging
            return None #if any error occurs return none 
    

    # fetch a menu item by its id
    def get_menu_by_id(self, menu_id):
        return Menu.query.get(menu_id) # get menu by primary key
    
    # fetch menu items for the specific restaurant 
    def get_menu_by_restaurant(self, restaurant_id, category='', type_filter=''):
        query = Menu.query.filter(and_(
            Menu.restaurant_id == restaurant_id,   # match restaurant id
            Menu.is_available == True # only include available items
        ))
        


        # filter if a category is provided
        if category:
            query = query.filter_by(category=category)
        #filter if a type 
        if type_filter:
            query = query.filter_by(type=type_filter)
        #return the filtered and sorted result
        return query.order_by(Menu.category, Menu.name).all()
    

    #fetch all distinct categories for a restaurant
    def get_categories_by_restaurant(self, restaurant_id):
        categories = db.session.query(Menu.category).filter(
            and_(Menu.restaurant_id == restaurant_id, Menu.is_available == True)# match restaurant id,only include if available
        ).distinct().all()
        return [category[0] for category in categories if category[0]]
    


    #fetch and update the menu item
    def update_menu(self, menu):
        try:
            db.session.commit() # commit the changes of the updated menu items 
            return menu #return the updated menu object
        except Exception as e:
            db.session.rollback() #if any error occurs rollback
            print(f"Error updating menu: {e}") #print the error for debugging
            return None # return none on failure
    



    #delete a menuitem by making it unavailable
    def delete_menu(self, menu_id):
        try:
            menu = Menu.query.get(menu_id)# get the menu item by id
            if menu:
                menu.is_available = False # make it as unavailable
                db.session.commit() # commit changes 
                return True 
            return False
        except Exception as e:
            db.session.rollback() # if any error occurs rollback
            print(f"Error deleting menu: {e}") #print error for debugging
            return False
    



    # search menuitems by the name with page support
    def search_menu_items(self, search_term, page=1, per_page=10):
        #filter items by name 
        query = Menu.query.filter(and_(
            Menu.name.ilike(f'%{search_term}%'), # partial match  of name
            Menu.is_available == True # only give available items
        ))
        # return paginated results
        return query.paginate(page=page, per_page=per_page, error_out=False)