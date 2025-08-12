from db import db # import db from db.py 

from datetime import datetime # import datetime to handle timestamp

class Menu(db.Model): # defines menu model class
    __tablename__ = 'menus' #it specifies model class name 
    
    id = db.Column(db.Integer, primary_key=True) # it is a menu id and it is a primary key

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False) # it is restaurant id and its is a foreign key 

    name = db.Column(db.String(100), nullable=False) # menu item name

    description = db.Column(db.Text, nullable=True) # description of the menu item

    price = db.Column(db.Float, nullable=False)# price of the item

    category = db.Column(db.String(50), nullable=True)# is it a main course ,starter,dessert

    type = db.Column(db.String(20), nullable=False, default='veg')  # veg, non-veg

    image = db.Column(db.String(200), nullable=True) # it ia an image of the  menu item 

    is_available = db.Column(db.Boolean, default=True) # it shows whether the item is available for the order or not 

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    def to_dict(self):   # convert menu item to a API response
        return {
            'id': self.id,
            'restaurant_id': self.restaurant_id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'type': self.type,
            'image': self.image,
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    

    #String represntation of the  menu object
    def __repr__(self):
        return f'<Menu {self.name}>'