from db import db #import db from db.py
#import models
from models.order import Order, OrderItem 
from models.restaurant import Restaurant

class OrderDAO: # defines data access object for order
    def create_order(self, order): #creating and saving a new order in database
        try:
            db.session.add(order) #add new orders
            db.session.commit() # commit changes after adding
            return order.id # return the order id 
        except Exception as e:
            db.session.rollback() # if any error occurs rollback
            print(f"Error creating order: {e}") # print error for debugging
            return None #return none
    

    #create and save new order item to database
    def create_order_item(self, order_item):
        try:
            db.session.add(order_item) # add orderitems 
            db.session.commit() # commit changes after adding 
            return order_item #return the created order item
        

        # if any error occurs roll back and print the error for debugging 
        except Exception as e:
            db.session.rollback() 
            print(f"Error creating order item: {e}")
            return None
    
    #get the order by using orderid
    def get_order_by_id(self, order_id):
        return Order.query.get(order_id)
    
    #get orders for the given page 
    def get_orders_by_user(self, user_id, page=1, per_page=10):
        try:
            # Get orders with proper pagination
            offset = (page - 1) * per_page
            orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).offset(offset).limit(per_page).all()
            total = Order.query.filter_by(user_id=user_id).count()
            
            print(f"Found {total} orders for user {user_id}")
            print(f"Returning {len(orders)} orders for page {page}")
            
            # Create pagination object to manage the paged results
            class SimplePagination:
                def __init__(self, items, total, page, per_page):
                    self.items = items #list of items on current page 
                    self.total = total # total number of items 
                    self.page = page #current page number
                    self.per_page = per_page #items per page 
                    self.pages = (total + per_page - 1) // per_page if total > 0 else 0
                    self.has_prev = page > 1 #has a previous page
                    self.has_next = page < self.pages #has a ext page
                    self.prev_num = page - 1 if self.has_prev else None #previous page number
                    self.next_num = page + 1 if self.has_next else None # next page number
                


                # iterate through page number
                def iter_pages(self):
                    for i in range(1, self.pages + 1):
                        yield i
            
            return SimplePagination(orders, total, page, per_page) # return paged object
        except Exception as e:
            print(f"Error fetching orders: {e}") # print error for the debugging 
            #return back  an empty page if any error occur
            class EmptyPagination:
                def __init__(self):
                    self.items = []
                    self.total = 0
                    self.pages = 0
                    self.page = page
                    self.per_page = per_page
                    self.has_prev = False
                    self.has_next = False
                    self.prev_num = None
                    self.next_num = None
                
                def iter_pages(self):
                    return []
            
            return EmptyPagination() #return empty page 
    
    #get orders by restaurant id 
    def get_orders_by_restaurant(self, restaurant_id, page=1, per_page=10):
        return Order.query.filter_by(restaurant_id=restaurant_id).order_by(Order.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        ) #uses build in paginate
    

    #update the status of an order 
    def update_order_status(self, order_id, status):
        try:
            order = Order.query.get(order_id)#get order by orderid
            if order:
                order.status = status #update the status 
                db.session.commit() #commit changes
                return order #return updated order
            return None
        except Exception as e:
            db.session.rollback()   #if any error occurs rollback 
            print(f"Error updating order status: {e}")# print the error for debugging
            return None
    

    #get all the orders in the syatem with pagination
    def get_all_orders(self, page=1, per_page=10):
        return Order.query.order_by(Order.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False #return paginated list
        )
    

    #order statistics
    def get_order_statistics(self, user_id=None, restaurant_id=None):
        query = Order.query # start with base query
        
        if user_id:
            query = query.filter_by(user_id=user_id) #filter by userid if given 
        
        if restaurant_id:
            query = query.filter_by(restaurant_id=restaurant_id) #filter by restaurant id if given 
        
        total_orders = query.count() #after filtering count the total orders

        #calculate total amount
        total_amount = db.session.query(db.func.sum(Order.total_amount)).filter(
            Order.user_id == user_id if user_id else True,
            Order.restaurant_id == restaurant_id if restaurant_id else True
        ).scalar() or 0
        
        return {
            'total_orders': total_orders,#total number of orders
            'total_amount': total_amount #total revenue amount
        }