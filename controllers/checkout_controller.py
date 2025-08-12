from flask import Blueprint, request, render_template, redirect, url_for, session, flash #import required modules from flask
from models.order import Order, OrderItem #import order models
from models.cart import Cart #import cart models
from db import db# import database
from dao.cart_dao import CartDAO #import cart dao
from dao.order_dao import OrderDAO #import oder dao
from datetime import datetime #import parsing data

checkout_bp = Blueprint('checkout', __name__) #blueprint for checkout
cart_dao = CartDAO()#instance for cart
order_dao = OrderDAO()#instrance for order
#route to display checkout page 
@checkout_bp.route('/checkout')
def checkout():
    #ensure user should be logged in
    if 'user_id' not in session:
        flash('Please login to checkout', 'error') #flash login message 
        return redirect(url_for('login.login'))#redirect to login page
    
    user_id = session['user_id'] #get userid from session
    cart_items = cart_dao.get_cart_items(user_id) #get all cart items for the user
    
    #if not cart item is found
    if not cart_items:
        flash('Your cart is empty', 'error')#flash a message cart is empty
        return redirect(url_for('cart.cart')) # redirect to cart
    #calculate total sum
    total = sum(item.menu.price * item.quantity for item in cart_items)
    #render checkout with cart data
    return render_template('checkout.html', cart_items=cart_items, total=total)
#route to handle order place ment after form submission
@checkout_bp.route('/place_order', methods=['POST'])
def place_order():
    #ensure user should be logged in
    if 'user_id' not in session:
        flash('Please login to place order', 'error') #flash a message 
        return redirect(url_for('login.login')) #redirect to login page 
    
    #get user id from session
    user_id = session['user_id']
    #while order booking 
    booking_name = request.form.get('booking_name')
    booking_email = request.form.get('booking_email')
    delivery_date_str = request.form.get('delivery_date')
    delivery_time = request.form.get('delivery_time')
    delivery_address = request.form.get('delivery_address')
    phone = request.form.get('phone')
    payment_method = request.form.get('payment_method')
    special_instructions = request.form.get('special_instructions')
    
    # Convert delivery_date string to date object
    delivery_date = None
    if delivery_date_str:
        try:
            delivery_date = datetime.strptime(delivery_date_str, '%Y-%m-%d').date()
        except ValueError:
            pass #ignore if date is invalid
    
    #verify required fields
    if not all([booking_name, delivery_address, phone, payment_method]):
        flash('Please fill in all required fields', 'error') #flash that fill the required fields
        return redirect(url_for('checkout.checkout')) #redirect to checkout
    
    #get cart items for user
    cart_items = cart_dao.get_cart_items(user_id)
    

    #check if cart is empty
    if not cart_items:
        flash('Your cart is empty', 'error') #if empty flash a message 
        return redirect(url_for('cart.cart')) #redirect to cart
    
    # Group items by restaurant
    restaurants_orders = {}
    for item in cart_items: #iterate  each item in the user cart
        restaurant_id = item.menu.restaurant_id #get restaurant id connected to cart items
        if restaurant_id not in restaurants_orders: #if the restaurant is not already in the dictionary ,add it with an empty
            restaurants_orders[restaurant_id] = []
        restaurants_orders[restaurant_id].append(item) #append the current cart item
    
    #list to store ids of placed orders
    order_ids = []
    
    # Create separate orders for each restaurant
    for restaurant_id, items in restaurants_orders.items():
        #calculate total amount
        total_amount = sum(item.menu.price * item.quantity for item in items)
        total_amount = total_amount * 1.05  # Add 5% tax
        
        # Create new  order instance 
        order = Order(
            user_id=user_id,
            restaurant_id=restaurant_id,
            total_amount=total_amount,
            delivery_address=delivery_address,
            phone=phone,
            payment_method=payment_method,
            booking_name=booking_name,
            booking_email=booking_email,
            delivery_date=delivery_date,
            delivery_time=delivery_time,
            special_instructions=special_instructions
        )
        
        # Save order to database
        try:
            db.session.add(order) # add order to the session
            db.session.flush()  # Get the order ID...save it temporarily
            order_id = order.id #get the new order id 
            print(f"Created order with ID: {order_id}") #print the id in the console
        except Exception as e:
            print(f"Error creating order: {e}") #print error --while creating order
            db.session.rollback() #if any error rollback
            continue #skip to the next order
        
        if order_id: #if order was created successfully
            order_ids.append(order_id) #save the order id in a list
            # Create order items
            for item in items:
                order_item = OrderItem( #create a new order item
                    order_id=order_id, #linik it to the current order 
                    menu_id=item.menu_id, # menu item id 
                    quantity=item.quantity,# quantity of the item
                    price=item.menu.price #price of the item
                )
                try:
                    db.session.add(order_item) # add the item to the database
                    print(f"Added order item: {item.menu.name} x {item.quantity}") #print a message 
                except Exception as e:
                    print(f"Error creating order item: {e}") # if any error occurs show error if failed 
    
    # Commit all changes
    try:
        db.session.commit() #finally save to the database
        print(f"Successfully saved {len(order_ids)} orders") #print succesful message 
    except Exception as e:
        print(f"Error committing orders: {e}") # show an error
        db.session.rollback() #if any error occurs undo everything 
        flash('Failed to place order. Please try again.', 'error') #flash a message that failed to palce an order
        return redirect(url_for('checkout.checkout')) #redirect to checkout page 
    
    # Clear cart after successful order
    cart_dao.clear_cart(user_id)
    
    flash(f'Order placed successfully! Order ID(s): {", ".join(map(str, order_ids))}', 'success') #flash success message if order id
    return redirect(url_for('order_history.order_history')) # redirect to order history page 