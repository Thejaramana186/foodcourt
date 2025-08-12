from db import db # import db from db.py

from datetime import datetime# import datetime  to handle timestamps

class Cart(db.Model): # defines cart model class
    __tablename__ = 'carts' #table name in the database
    
    id = db.Column(db.Integer, primary_key=True) #cart id it is a primary key

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # user id is a foreign key linking to the  cart

    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=False) #menu id is a foreign key it linked to the cart 

    quantity = db.Column(db.Integer, nullable=False, default=1) # number of units of the item

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    

    # Relationship between  cart and menu 
    menu = db.relationship('Menu', backref='cart_items', lazy=True)
    
    # convert cart item to a dictionary 
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'menu_id': self.menu_id,
            'quantity': self.quantity,
            'menu': self.menu.to_dict() if self.menu else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    # string representation of the cart object
    def __repr__(self):
        return f'<Cart {self.id}>'