from flask_sqlalchemy import SQLAlchemy # import the sqlalchemy

db = SQLAlchemy() # instance of sqlalchemy

def init_db(app): # function to initialize the database with flask app
    db.init_app(app) # instance to the flask appbind the sqlalchemy
    with app.app_context(): #create an application context
        db.create_all()#create all the tables in the database based on defined models