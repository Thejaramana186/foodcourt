from db import db # import db from db.py

from models.user import User # import the user model

class UserDAO: # defines data access object for user
       
    def create_user(self, user): # create new user and add to the database
        try:  # try block
            db.session.add(user) #add's user to the current database

            db.session.commit() #it is to savethe commited changes 

            return user  # returns created user object
        except Exception as e:
            db.session.rollback() # if there is any exception occurs rollback and change

            print(f"Error creating user: {e}") #show a message if something goes wrong while creating user object  

            return None # returns none on failure 
    
    def get_user_by_id(self, user_id): # retrives user by their id
        return User.query.get(user_id) 
    
    def get_user_by_username(self, username):# retrives user by their username
        return User.query.filter_by(username=username).first()
    
    def get_user_by_email(self, email):#retrives user by their email
        return User.query.filter_by(email=email).first()
    
    def update_user(self, user): # updates user information 
        try:
            db.session.commit() # commit changes if any updates available 
            return user  # return updated user object
        except Exception as e:
            db.session.rollback() #if there is any exception occurs rollback
            print(f"Error updating user: {e}")# show a message if some error occurs
            return None # returns none on failure
    
    def delete_user(self, user_id): # delete an user by there user_id
        try:
            user = User.query.get(user_id) # fetch user by user_id
            if user:
                db.session.delete(user) # delete user
                db.session.commit() #commit the deletion 
                return True # return success 
            return False # is failure return failure
        except Exception as e:
            db.session.rollback() #any exception rollback to the error
            print(f"Error deleting user: {e}")#show a message if any error occurs 
            return False #return failure 
    


    #fetch a specifix page of users from the database with a number per page 
    def get_all_users(self, page=1, per_page=10):
        return User.query.paginate(page=page, per_page=per_page, error_out=False) # pagination to avoid loading all the users at once 