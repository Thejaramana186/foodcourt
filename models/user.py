from db import db     # immport db from db.py
from datetime import datetime   # import datetime when the user created the account
from werkzeug.security import generate_password_hash, check_password_hash # import password hashing 

class User(db.Model):  #defining the user model class
    __tablename__ = 'users'  # defining the name of the table in database
    
    id = db.Column(db.Integer, primary_key=True)  # user id column which is primary key and auto incrementing 

    username = db.Column(db.String(80), unique=True, nullable=False)  #username which should not be same and not to be null

    email = db.Column(db.String(120), unique=True, nullable=False) # email must be unique 

    password_hash = db.Column(db.String(128), nullable=False) # password should not be null

    phone = db.Column(db.String(20), nullable=True) 

    address = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow) # it is when the user was created the account
    
   
    carts = db.relationship('Cart', backref='user', lazy=True, cascade='all, delete-orphan')  #it is for allow the cart to refer its user and delete all the users carts is user is deleted 

    orders = db.relationship('Order', backref='user', lazy=True, cascade='all, delete-orphan') #it allows order to reference its user , load and delete all the users orders if user is deleted
    
    #this is to hash and store the password
    def set_password(self, password):  
        self.password_hash = generate_password_hash(password)
    

    # this is confirm or check the password 
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    #convert user object to dictionary for JSON
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'