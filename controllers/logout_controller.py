from flask import Blueprint, redirect, url_for, session, flash   # import required modules froom flask

logout_bp = Blueprint('logout', __name__) # bluprint for logout related routes

@logout_bp.route('/logout') # route for logout url 
def logout():
    #clear all the data
    session.clear()
    #flash a message that 'you are successfully logout '
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('index')) # redirect to home page (home page is noting but index)