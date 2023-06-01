from . import api
from flask import request
import requests
import json
# we will import some Models here and Authorize the user first. BUT
from ..apiauthhelper import token_auth
from ..models import Bathroom, RecentSearch, SearchedBathroom
from sqlalchemy import desc, func
from datetime import datetime, timedelta # for deleting objects

@api.get('recent-search/all')
@token_auth.login_required
def getRecentSearchesAPI():
    # print("hi")
    user = token_auth.current_user() 
    # print("user is " + user.email)
    #user = User.query.filter_by(user_id=1).first()
    # searched_bathrooms = SearchedBathroom.query.filter_by()
    #Cart.query.filter_by(user_id=user_id).all()  # actually gets us every item 
    
    if user:
        searches = []
        recent_search_locs = RecentSearch.query.filter_by(user_id = user.user_id).order_by(desc(RecentSearch.time_searched)).all()
        for loc in recent_search_locs:
            loc_dict = loc.to_dict()
            
            # print(loc.to_dict())
            # searched_bathrooms = SearchedBathroom.query.filter_by(search_id = )
            bathrooms = []
            searched_bathrooms = SearchedBathroom.query.filter_by(search_id = loc.search_id)
            for searched_bathroom in searched_bathrooms:
                bathroom = Bathroom.query.get(searched_bathroom.bathroom_id)
                bathrooms.append(bathroom.to_dict())
            
            loc_dict['bathrooms'] = bathrooms
            searches.append(loc_dict)
        return {
            'status' : 'ok',
            'message' : 'Successfully retrieved the recent searches',
            'data' : searches,
            'last_search_id' : RecentSearch.query.filter_by(user_id = user.user_id).order_by(desc(RecentSearch.time_searched)).first().search_id
        }
    else:
        return {
            'status' : 'not ok',
            'message' : 'No user is logged in.'
        }



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
            # print("This is the last added location: ")
            # print(last_added.to_dict())
            # if the next search is the same as the last one 
            # print(f"origin_name: {origin_name}\norigin_address: {origin_address}\ndestination_name: {destination_name}\n{destination_address}")
            if last_added:
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
            print(data)
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
    

@api.delete('recent-search/delete-all')
def deleteOldSearchesAPI():
    oldest_allowed = datetime.utcnow() - timedelta(weeks=1)
    # print(oldest_allowed)
    # r = RecentSearch.query.get(1).time_searched
    # print(r)
    if RecentSearch.query.first():
        # print(r < oldest_allowed) # is r young enough a search
        too_old = RecentSearch.query.filter(RecentSearch.time_searched < oldest_allowed).delete()
        RecentSearch.save_changes_to_db(RecentSearch)
        if too_old:
            return {
                'status' : 'ok',
                'message' : 'Successfully deleted all recent history from over a week ago.',
                # 'data_deleted' : [search.to_dict() for search in too_old]
            }
        else:
            return {
                'status' : 'not ok',
                'message' : 'There was nothing old enough to delete',
                # 'data_deleted' : [search.to_dict() for search in too_old]
            }
    else:
        return {
                'status' : 'not ok',
                'message' : 'There was nothing in the search history',
                # 'data_deleted' : [search.to_dict() for search in too_old]
            }