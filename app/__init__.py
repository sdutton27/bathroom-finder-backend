from flask import Flask
from config import Config
from .models import db
from flask_migrate import Migrate 
from flask_cors import CORS
from .api import api #coming from the init file , so just api

app = Flask(__name__)
app.config.from_object(Config)

cors = CORS()
cors.init_app(app)

migrate = Migrate(app,db)
db.init_app(app)

# register blueprints
app.register_blueprint(api)

from . import routes
from . import models # new with forms
