from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')

from . import auth_routes
from . import bathroom_routes
from . import places_routes
from . import favorites_routes 
from . import recent_search_routes