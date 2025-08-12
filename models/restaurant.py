from db import db  # import db connection from db.py

from datetime import datetime # import datetime 

class Restaurant(db.Model): # define the restaurant class form SQLalchemy's model
    __tablename__ = 'restaurants' # defines the name of the database table 
    
    id = db.Column(db.Integer, primary_key=True) # it is a restaurant id column and it is primary key

    name = db.Column(db.String(100), nullable=False) #restaurant name 

    cuisine = db.Column(db.String(50), nullable=False) #cuisine type

    rating = db.Column(db.Float, default=0.0)# restaurant rating  default it will be in float

    delivery_time = db.Column(db.String(20), nullable=True) # estimated delivery time 

    image = db.Column(db.String(200), nullable=True) # image of the restaurant

    type = db.Column(db.String(20), nullable=False, default='both')  # veg, non-veg, both

    address = db.Column(db.Text, nullable=True) #restaurant address

    phone = db.Column(db.String(20), nullable=True) # restaurant phone number

    is_active = db.Column(db.Boolean, default=True)# it shows is the restaurant is active or not

    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
    
    
    menus = db.relationship('Menu', backref='restaurant', lazy=True, cascade='all, delete-orphan')#it is the relation between restaurant and menu because there will be more menu items for one restaurant
    
    # convert resturant object to useful API's
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cuisine': self.cuisine,
            'rating': self.rating,
            'delivery_time': self.delivery_time,
            'image': self.image,
            'type': self.type,
            'address': self.address,
            'phone': self.phone,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Restaurant {self.name}>'