#import all useful modules from flask like render_template,redirect,flash....
from flask import Blueprint, request, render_template, redirect, url_for, session, flash
#import the user  from model
from models.user import User
#import the userdao classes for the database access
from dao.user_dao import UserDAO



#blue print for login related routes
login_bp = Blueprint('login', __name__)
#instance of the userdao to interact with the user table
user_dao = UserDAO()


#defining the route for login for both GET and POST 
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    #if the request is a post - form submitted
    if request.method == 'POST':
        #get the username and password from the form
        username = request.form.get('username')
        password = request.form.get('password')
        

        #checking either field isempty 
        if not username or not password: 
            flash('Please fill in all fields', 'error') #flash error message 
            return render_template('login.html') #return or reload the login page 
        

        #it fetches the user from database using username
        user = user_dao.get_user_by_username(username)
        
        #suppose if the user exists and the password matches
        if user and user.check_password(password):
            #stthis section will be logged in
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success') #flashes success message 
            return redirect(url_for('index')) #redirects to homepage
        else:
            flash('Invalid username or password', 'error') # if any errors or fails to login show the error
    
    return render_template('login.html') #redirect to login page