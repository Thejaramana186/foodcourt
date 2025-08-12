from flask import Blueprint, request, render_template, redirect, url_for, session, flash, jsonify #import required modules from the flask
from models.cart import Cart # import cart model
from models.menu import Menu#import menu model
from dao.cart_dao import CartDAO #import cartdao to interact with database

cart_bp = Blueprint('cart', __name__) #blueprint for cart related routes
cart_dao = CartDAO() #instance for cartdao to interact with database



#route to view cart items 
@cart_bp.route('/cart')
def cart():
    #check if user is logged in 
    if 'user_id' not in session:
        flash('Please login to view your cart', 'error') #flash a message to login 
        return redirect(url_for('login.login')) #redirect to login page
    
    user_id = session['user_id'] #get login user id
    cart_items = cart_dao.get_cart_items(user_id) #get cart items from the database
    
    total = sum(item.menu.price * item.quantity for item in cart_items)#  calculate total price of cart items
    
    return render_template('cart.html', cart_items=cart_items, total=total) #render the cart with items and total
  #route to add an item to the cart
@cart_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    #check does the user logged in or not
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401
    #get user id from the session
    user_id = session['user_id']
    menu_id = request.json.get('menu_id') #extract menuid and quantity
    quantity = request.json.get('quantity', 1)
    
    #verify that menuid is provided 
    if not menu_id:
        return jsonify({'error': 'Menu ID is required'}), 400
    
    
    # Check if menu item exists
    menu_item = Menu.query.get(menu_id)
    if not menu_item:
        return jsonify({'error': 'Menu item not found'}), 404
    
    # Add to cart
    cart_item = cart_dao.add_to_cart(user_id, menu_id, quantity)
    #return success or failure response
    if cart_item:
        return jsonify({'message': 'Item added to cart successfully', 'cart_item': cart_item.to_dict()})
    else:
        return jsonify({'error': 'Failed to add item to cart'}), 500



#route to update the cart quantity or remove item
@cart_bp.route('/update_cart', methods=['POST'])
def update_cart():
    #ensure user is logged in
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401
    #get user id from session
    user_id = session['user_id']
    #extract cartid and quantity
    cart_id = request.json.get('cart_id')
    quantity = request.json.get('quantity')
    #verify the input
    if not cart_id or quantity is None:
        return jsonify({'error': 'Cart ID and quantity are required'}), 400
    
    #suppose the quantity is zero or less than zero ,from the item from the cart
    if quantity <= 0:
        # Remove item from cart
        if cart_dao.remove_from_cart(user_id, cart_id):
            return jsonify({'message': 'Item removed from cart'})
        else:
            return jsonify({'error': 'Failed to remove item from cart'}), 500
    else:
        # Update quantity
        cart_item = cart_dao.update_cart_quantity(user_id, cart_id, quantity)
        if cart_item:
            return jsonify({'message': 'Cart updated successfully', 'cart_item': cart_item.to_dict()})
        else:
            return jsonify({'error': 'Failed to update cart'}), 500


#route to remove item from the cart
@cart_bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    #ensure user is logged in
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401
    
    #get user id 
    user_id = session['user_id']
    cart_id = request.json.get('cart_id') # extract cart id 
    
    #verify cart id
    if not cart_id:
        return jsonify({'error': 'Cart ID is required'}), 400
    #remove the item from cart 
    if cart_dao.remove_from_cart(user_id, cart_id):
        return jsonify({'message': 'Item removed from cart successfully'})
    else:
        return jsonify({'error': 'Failed to remove item from cart'}), 500


#route to clear all items from the cart 
@cart_bp.route('/clear_cart', methods=['POST'])
def clear_cart():
    #ensure user should be logged in
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401
    
    #get user id from session
    user_id = session['user_id']
    #clear all the cart items 
    if cart_dao.clear_cart(user_id):
        return jsonify({'message': 'Cart cleared successfully'})
    else:
        return jsonify({'error': 'Failed to clear cart'}), 500