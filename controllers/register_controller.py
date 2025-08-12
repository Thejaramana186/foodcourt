from flask import Blueprint, request, render_template, redirect, url_for, flash
#import required modules from flask
#import user model 
from models.user import User
#import userdao
from dao.user_dao import UserDAO

register_bp = Blueprint('register', __name__) #blueprint for registration related routes
user_dao = UserDAO() #instance of userdao



#defines routes for user registration handles both get and post
@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    #if the form is submitted-post
    if request.method == 'POST':
        #take from data
        username = request.form.get('username') #get username
        email = request.form.get('email') #get email
        password = request.form.get('password') #get password
        confirm_password = request.form.get('confirm_password') #confirm password
        phone = request.form.get('phone')#get phone number
        address = request.form.get('address')#addres
        
        # Validation
        #first ensure all the fields are filled
        if not all([username, email, password, confirm_password]):
            flash('Please fill in all required fields', 'error') #show an error if any thing is not filled 
            return render_template('register.html') # redirect or reload register page
        
        if password != confirm_password:  #ensure password match
            flash('Passwords do not match', 'error') #show mismatch error
            return render_template('register.html') #redirect or reload register page
        
        # Check if user already exists in database
        if user_dao.get_user_by_username(username):
            flash('Username already exists', 'error')#flash invalid error
            return render_template('register.html') # reload register page 
        
        if user_dao.get_user_by_email(email): # check email already exists in database or not 
            flash('Email already exists', 'error') #flash email already exist
            return render_template('register.html') #reload register page
        
        # Create new user
        user = User(
            username=username,
            email=email,
            phone=phone,
            address=address
        )
        #hash and set the password securely
        user.set_password(password)
        

        #save the new user in the database
        if user_dao.create_user(user):
            flash('Registration successful! Please login.', 'success') #flash successful message 
            return redirect(url_for('login.login')) #redirect to login page 
        else:
            flash('Registration failed. Please try again.', 'error') # flash failure message 
    return render_template('register.html')