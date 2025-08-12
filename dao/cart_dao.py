from db import db # import db from db.py
from models.cart import Cart # import cart model
from models.menu import Menu # import menu model
from sqlalchemy import and_   #import and_ for combining sqlalchemy filter condition

class CartDAO: # dao for cart 




    #add an item to cart method 
    def add_to_cart(self, user_id, menu_id, quantity=1):
        try:
            # Check if item already exists in cart
            existing_cart = Cart.query.filter(and_(
                #match by userid and match by menu item id
                Cart.user_id == user_id, 
                Cart.menu_id == menu_id
            )).first()
            


            # if iteam already exists,increase its quantity
            if existing_cart:
                existing_cart.quantity += quantity
                db.session.commit() #commit changes
                return existing_cart # return updated cart item
            else:
                #if items does not exist ,create a new cart entry
                cart = Cart(
                    user_id=user_id,
                    menu_id=menu_id,
                    quantity=quantity
                )
                db.session.add(cart) #add new cart item
                db.session.commit()  #commit changes
                return cart  # return new cart item
        except Exception as e:
            db.session.rollback() # if any error occurs roll back
            print(f"Error adding to cart: {e}") #print the error for debugging
            return None
    



    # method for getting all  cart items for the user
    def get_cart_items(self, user_id):
        return Cart.query.filter_by(user_id=user_id).join(Menu).all() # fetch cart items joined with menu data
    

    


    # method to update the quantity of the specific cart item
    def update_cart_quantity(self, user_id, cart_id, quantity):
        try:
            #get teh specific cart item for the user   ----it match cart id,match user id
            cart = Cart.query.filter(and_(
                Cart.id == cart_id,
                Cart.user_id == user_id
            )).first()
            
            if cart:
                cart.quantity = quantity #update the quantity
                db.session.commit() #commit changes
                return cart # return updated cart items
            return None
        except Exception as e:
            db.session.rollback() #rollback on error
            print(f"Error updating cart quantity: {e}") #print  error for debugging
            return None #return none on failure
    


    #method to remove a specific item from the cart
    def remove_from_cart(self, user_id, cart_id):
        try:
            #find the specific cart item for the user----match cartid,match userid
            cart = Cart.query.filter(and_(
                Cart.id == cart_id,
                Cart.user_id == user_id
            )).first()
            
            if cart:
                db.session.delete(cart) #delete the cart item
                db.session.commit() #commit changes
                return True #return sucess
            return False
        except Exception as e:
            db.session.rollback() # if any error occurs rollback
            print(f"Error removing from cart: {e}") #print the error for debugging 
            return False
    #method to clear the entire the cart of the user
    def clear_cart(self, user_id):
        try:
            Cart.query.filter_by(user_id=user_id).delete() #delete all the user's cart items
            db.session.commit() #commit changes
            return True # return success
        except Exception as e:
            db.session.rollback() #if any error occurs rollback
            print(f"Error clearing cart: {e}")#print the error foe debugging 
            return False #return failure
    




    # method to calculate total price of the cart item of user
    def get_cart_total(self, user_id):
        cart_items = self.get_cart_items(user_id) #get all the cart items
        return sum(item.menu.price * item.quantity for item in cart_items) #sum the total by multiplying price for each item
    

    #method to count total items in the cart for the user
    def get_cart_count(self, user_id):
        return Cart.query.filter_by(user_id=user_id).count() #return number of cart items 