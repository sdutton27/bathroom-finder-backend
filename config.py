import os 
basedir = os.path.abspath(os.path.dirname(__name__)) # (gets you base directory for config.py)
class Config():
    FLASK_APP = os.environ.get('FLASK_APP') # what is the entrypoint to the application
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG') # could hardcode this in as 'development'
    SECRET_KEY = os.environ.get('SECRET_KEY') # make sure we have named this in .env
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') # make sure we have gotten the URL in .env
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10