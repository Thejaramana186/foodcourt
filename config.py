import os #import os module to access variables

class Config:
    #secret key used for securely signing the session 
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    #database connection uri
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///foodapp.db'
    #disable tracking modification to save system resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    SESSION_TYPE = 'filesystem' # stores session data in the file system
    SESSION_PERMANENT = False # make session non permanent
    SESSION_USE_SIGNER = True #sign session cookies for added security
    SESSION_KEY_PREFIX = 'foodapp:' # to avoid conflicts
    
    # Upload configuration
    UPLOAD_FOLDER = 'static/uploads' # folder path to store uploaded files
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # max upload size is 16mb