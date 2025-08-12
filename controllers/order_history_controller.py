from flask import Blueprint, request, render_template, redirect, url_for, session, flash
#import required modules from flask
from db import db #import db
from dao.order_dao import OrderDAO #import orderdao for database related to orders

order_history_bp = Blueprint('order_history', __name__) #blueprint for history related 
order_dao = OrderDAO() # instance of thr orderdao to interact with the database

@order_history_bp.route('/order_history') # route to display user order history
def order_history():
    #check if the user is logged in by verifying 
    if 'user_id' not in session: 
        flash('Please login to view order history', 'error') # show error message 
        return redirect(url_for('login.login')) #redirect to login page
    

    #get current user id from session 
    user_id = session['user_id']
    #get ths page number from the requested query
    page = request.args.get('page', 1, type=int)
    #print the message 
    print(f"Fetching order history for user ID: {user_id}")
    
    #try to retrive paginated order data using the dao
    try:
        orders = order_dao.get_orders_by_user(user_id, page=page, per_page=10)  #fetch user orders
        print(f"Retrieved {orders.total} total orders, {len(orders.items)} on current page")#print the log
    except Exception as e:
        print(f"Error fetching orders: {e}")# if any error occurs print the message for debugging 
        # Create simple empty pagination object
        class EmptyPagination:
            def __init__(self):
                self.items = []
                self.total = 0
                self.pages = 0
                self.page = page
                self.per_page = 10
                self.has_prev = False
                self.has_next = False
                self.prev_num = None
                self.next_num = None
            # dummy iterator for the page number
            def iter_pages(self):
                return []
        #empty paginated result as fallback
        orders = EmptyPagination()
        #flash message tothe user on failure
        flash('Unable to load order history. Please try again later.', 'error')
    #render the order history with the retrived orders
    return render_template('order_history.html', orders=orders)
#route to show details for a specific order by id
@order_history_bp.route('/order/<int:order_id>')
def order_detail(order_id):
    #check if the user is logged in
    if 'user_id' not in session:
        flash('Please login to view order details', 'error')#flash a message 
        return redirect(url_for('login.login'))#redirect to login page 
    #geyt the user id from session
    user_id = session['user_id']
    order = order_dao.get_order_by_id(order_id)#fetch the order by id
    
    #check if order exists and belongs to current user
    if not order or order.user_id != user_id:
        flash('Order not found', 'error')#flash a message if unauthorized or not found
        return redirect(url_for('order_history.order_history'))#redirect to order history page 
    #render the order details with the selected order
    return render_template('order_detail.html', order=order)