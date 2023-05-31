from . import api
from flask import request
import requests
import json
# we will import some Models here and Authorize the user first. BUT
from ..apiauthhelper import token_auth
from ..models import Bathroom, RecentSearch
from sqlalchemy import desc, func

# @api.post('recent-search/location/<string:origin_name>/<string:origin_address>/<string:destination_name>/<string:destination_address>')
# @api.post('recent-search/location/<string:origin_name>/<string:origin_address>')
@api.post('recent-search/location')
@token_auth.login_required
def saveRecentSearchLocAPI():
    user = token_auth.current_user() 
    data = request.json
    if user:
        if data:
            origin_name = data['origin_name']
            origin_address = data['origin_address']
            destination_name = data['destination_name']
            destination_address = data['destination_address']
            photo_base_64 = data['photo_base_64']

            last_added = RecentSearch.query.order_by(desc(RecentSearch.time_searched)).first()
            print("This is the last added location: ")
            print(last_added.to_dict())
            # if the next search is the same as the last one 
            print(f"origin_name: {origin_name}\norigin_address: {origin_address}\ndestination_name: {destination_name}\n{destination_address}")

            if (last_added.origin_name == origin_name and last_added.origin_address == origin_address 
                # and last_added.destination_name == destination_name and last_added.destination_address == destination_address
                ):
                return {
                    'status' : 'not ok',
                    'message' : 'This location is the same as the last searched.',
                    'data' : last_added.to_dict()
                }


            new_search = RecentSearch(user.user_id, origin_name, origin_address, photo_base_64, destination_name, destination_address)
            new_search.save_to_db()
            return {
                'status' : 'ok',
                'message' : 'Successfully added location(s) to a recent search.',
                'data' : new_search.to_dict()
            }
        else:
            return {
                'status' : 'not ok',
                'message' : 'Body not readable to input information.'
            }
    else:
        return {
            'status' : 'not ok',
            'message' : 'That user does not exist.'
        }

@api.post('recent-search/bathroom')
@token_auth.login_required
def saveRecentSearchBathroomAPI():
    user = token_auth.current_user() 
    data = request.json
    if user:
        if data:
            search_id = data['search_id']
            bathroom_id = data['bathroom_id']
            recent_search = RecentSearch.query.get(search_id)

            # last_searched_bathroom = RecentSearch.query.filter_by(search_id = search_id).order_by(desc(RecentSearch.time_searched).first())

            # last_searched_bathroom = RecentSearch.query(func.max(RecentSearch.time_searched)) 

            # subquery = RecentSearch.query(func.max(RecentSearch.time_searched)).filter(RecentSearch.search_id == search_id)
            last_searched_bathroom = recent_search.get_latest_search()

            bathroom = Bathroom.query.get(bathroom_id)

            print(last_searched_bathroom)
            if (not last_searched_bathroom or last_searched_bathroom['bathroom_id'] != bathroom_id):
                recent_search.add_searched_bathroom(bathroom_id)
                recent_search.save_to_db()
                return {
                    'status' : 'ok',
                    'message' : 'Successfully added bathroom to recent search.',
                    'data' : {
                        'recent_searches' : recent_search.searched_bathrooms_to_list(),
                        'bathroom' : bathroom.to_dict()
                    }
                }
            else:
                return {
                    'status' : 'not ok',
                    'message' : 'This bathroom was already your most recently searched',
                    'data' : recent_search.searched_bathrooms_to_list()
                }
            
            # if (last_searched_bathroom.bathroom_id == bathroom_id):
            #     return {
            #         'status' : 'not ok',
            #         'message' : 'This bathroom was already your most recently searched',
            #         'data' : recent_search.searched_bathrooms_to_list()
            #     }
            # else: 
            #     recent_search.add_searched_bathroom(bathroom_id)
            #     recent_search.save_to_db()
            #     return {
            #         'status' : 'ok',
            #         'message' : 'Successfully added bathroom to recent search.',
            #         'data' : recent_search.searched_bathrooms_to_list()
            #     }
        else:
            return {
                'status' : 'not ok',
                'message' : 'The proper search information has not been given.'
            }
    else:
        return {
            'status' : 'not ok',
            'message' : 'The user is either not logged in or not in the database.'
        }