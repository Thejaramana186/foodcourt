from db import db # import db connection from db.py

from datetime import datetime #import datetime

class Order(db.Model):  #define the order model from SQLAlchemy's

    __tablename__ = 'orders'  # table name for this model
    
    id = db.Column(db.Integer, primary_key=True) # it is order id and it is a primary key

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)#it is a user_id and it is a foreign key

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False) # it is restaurant_id and it is a foreign key 

    total_amount = db.Column(db.Float, nullable=False) # total_amount of a order 

    status = db.Column(db.String(50), nullable=False, default='pending')  # pending, confirmed, preparing, delivered, cancelled

    booking_name = db.Column(db.String(100), nullable=True)   #customer name 

    booking_email = db.Column(db.String(120), nullable=True) # customer email

    delivery_date = db.Column(db.Date, nullable=True) # order delivery date 

    delivery_time = db.Column(db.String(20), nullable=True)#order delivery time 

    delivery_address = db.Column(db.Text, nullable=True)# customer address

    phone = db.Column(db.String(20), nullable=True) # phone number of the customer

    payment_method = db.Column(db.String(50), nullable=True)#mode of payment

    special_instructions = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow) 


    restaurant = db.relationship('Restaurant', backref='orders', lazy=True) # relation that is  order belongs to which restaurant 

    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan') # reation that is one order has many order items 
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'restaurant_id': self.restaurant_id,
            'total_amount': self.total_amount,
            'status': self.status,
            'booking_name': self.booking_name,
            'booking_email': self.booking_email,
            'delivery_date': self.delivery_date.isoformat() if self.delivery_date else None,
            'delivery_time': self.delivery_time,
            'delivery_address': self.delivery_address,
            'phone': self.phone,
            'payment_method': self.payment_method,
            'special_instructions': self.special_instructions,
            'restaurant': self.restaurant.to_dict() if self.restaurant else None,
            'order_items': [item.to_dict() for item in self.order_items],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    #string represntation of the order object
    def __repr__(self):
        return f'<Order {self.id}>'


class OrderItem(db.Model): #defines orderitem
    __tablename__ = 'order_items' # name of table 
    
    id = db.Column(db.Integer, primary_key=True) # id of the orderitem it is a primary key 

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False) # it is a order id it is a foreign key

    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=False)# menu id is a foreign key 

    quantity = db.Column(db.Integer, nullable=False) # number of units has been ordered

    price = db.Column(db.Float, nullable=False)# price of the item
    
    
    menu = db.relationship('Menu', backref='order_items', lazy=True) # it is a relation between order item and menu item
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'menu_id': self.menu_id,
            'quantity': self.quantity,
            'price': self.price,
            'menu': self.menu.to_dict() if self.menu else None
        }
    
    #string representation of the orderitem object
    def __repr__(self):
        return f'<OrderItem {self.id}>'