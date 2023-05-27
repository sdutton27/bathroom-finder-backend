from . import api
from ..models import User
from flask import request
from ..apiauthhelper import token_auth

@api.get('favorites')
@token_auth.login_required
def getFavoritesAPI():
        user = token_auth.current_user() 
        print("user is " + user.email)
        #user = User.query.filter_by(user_id=1).first()
        
        #Cart.query.filter_by(user_id=user_id).all()  # actually gets us every item 
        

        return {
            'status':'ok',
            'favorites': user.favorites_to_list()
        }

# @api.get('favorite/<int:bathroom_id>')
# @token_auth.login_required
# def favoriteBathroomAPI():