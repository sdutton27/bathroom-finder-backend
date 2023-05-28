from . import api
from ..models import User, Bathroom
from flask import request
from ..apiauthhelper import token_auth

@api.get('favorites')
@token_auth.login_required
def getFavoritesAPI():
    # print("hi")
    user = token_auth.current_user() 
    # print("user is " + user.email)
    #user = User.query.filter_by(user_id=1).first()
    
    #Cart.query.filter_by(user_id=user_id).all()  # actually gets us every item 
    if user:
        return {
            'status':'ok',
            'favorites': user.favorites_to_list(),
        }
    else:
        return {
            'status' : 'not ok',
            'message' : 'No user is logged in.'
        }


@api.post('favorites/favorite/<int:bathroom_id>')
@token_auth.login_required
def favoriteBathroomAPI(bathroom_id):
    bathroom = Bathroom.query.get(bathroom_id)
    user = token_auth.current_user() 

    if user:
        if bathroom:
            user.favorite(bathroom) # changes already saved
            return {
                'status' : 'ok',
                'message' : f"Successfully favorited bathroom {bathroom_id}",
                'favorites' : user.favorites_to_list()
            }
        else:
            return {
                'status' : 'not ok',
                'message' : 'Bathroom not found.'
            }
    else:
        return {
            'status' : 'not ok',
            'message' : 'User not found.'
        }


@api.delete('favorites/unfavorite/<int:bathroom_id>')
@token_auth.login_required
def unfavoriteBathroomAPI(bathroom_id):
    bathroom = Bathroom.query.get(bathroom_id)
    user = token_auth.current_user() 

    if user:
        if bathroom:
            user.unfavorite(bathroom) # changes already saved
            return {
                'status' : 'ok',
                'message' : f"Successfully unfavorited bathroom {bathroom_id}",
                'favorites' : user.favorites_to_list()
            }
        else:
            return {
                'status' : 'not ok',
                'message' : 'Bathroom not found.'
            }
    else:
        return {
            'status' : 'not ok',
            'message' : 'User not found.'
        }
