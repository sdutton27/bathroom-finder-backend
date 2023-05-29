from . import api
from flask import request
import requests
import json
# we will import some Models here and Authorize the user first. BUT
from ..apiauthhelper import token_auth
from ..models import Bathroom

@api.get('search-around-loc/<string:lat>/<string:lng>/<string:north>/<string:east>/<string:south>/<string:west>')
def getBathroomsAroundLoc(lat, lng, north, east, south, west):
    # NOTE HOW THIS IS JUST ONE PAGE'S WORTH RIGHT NOW... WE WILL HAVE TO CONTINUE THIS WITH MULTIPLE PAGES AND ALSO PASS THAT IN
    
    # Just going through the 26 closest bathrooms... I feel like that is enough options
    url = f"https://www.refugerestrooms.org/api/v1/restrooms/by_location?page=1&per_page=26&offset=0&lat={lat}&lng={lng}"
    response = requests.get(url)
    data = response.json()
    print(type(data))
    # dict = json.loads({'data' : data})
    # print(dict['data'])
    # print(type(dict['data']))

    # n_reached = False 
    # e_reached = False 
    # s_reached = False 
    # w_reached = False

    # convert everything to floats 
    lat = float(lat)
    lng = float(lng)
    north = float(north)
    east = float(east)
    west = float(west)
    south = float(south)

    print(lat)
    print(type(lat))

    i = 0

    bathrooms_in_range = []

    lat_in_range = True
    lng_in_range = True 
    # while ((not n_reached or not e_reached or not s_reached or not w_reached) and i < 26):
    
    print(type(data[0]['latitude']))

    while i < 26 and i < len(data): # goes through up to 26, but limited if the results are under 26
        try:
            
            # print('latitude at location : ' + str(data[i]['latitude']))
            # print('longitude at location : ' + data[i]['longitude'])

            # START WITH LATITUDE
            if lat > 0.0: # positive lat 
                # if data[i]['latitude'] > north or data[i]['latitude'] < south:
                #     lat_in_range = False
                # else:
                #     lat_in_range = True 
                lat_in_range = data[i]['latitude'] < north and data[i]['latitude'] > south
            else: # negative lat 
                # if data[i]['latitude'] < north or data[i]['latitude'] > south:
                #     lat_in_range = False
                # else:
                #     lat_in_range = True
                lat_in_range = data[i]['latitude'] > north and data[i]['latitude'] < south
            # CHECK LONGITUDE -- note that both positive and negative are the same 
            # if data[i]['longitude'] > east or data[i]['longitude'] < west:
            #     lng_in_range = False
            # else:
            #     lng_in_range = True 
            
            lng_in_range = data[i]['longitude'] < east and data[i]['longitude'] > west

            # print('lng in range:')
            # print(lng_in_range)
            # print('lat in range:')
            # print(lat_in_range)

            # if item is in range, add it to list
            if lng_in_range and lat_in_range:
                
                bathrooms_in_range.append(data[i])

            # go to the next item 
            print(i)
            i+= 1
        except:
            break # if that was the end of the breakpoint 
    # url = f"https://www.refugerestrooms.org/api/v1/restrooms/by_location?page=1&per_page=10&offset=0&lat={lat}&lng={lng}"
    
    # response = requests.get(url)
    # data = response.json()

    # print(data)
    return {
        'status' : 'ok',
        'number_of_results' : len(bathrooms_in_range),
        'results' : bathrooms_in_range,
    }

#     bathroom_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
#     name = db.Column(db.String(45), nullable=False)
#     street = db.Column(db.String(45), nullable=False)
#     city = db.Column(db.String(45), nullable=False)
#     state = db.Column(db.String(2), nullable=True) --- INCLUDED THIS 
#     country = db.Column(db.String(15), nullable=False)
#     accessible = db.Column(db.Boolean, nullable=False)
#     unisex = db.Column(db.Boolean, nullable=False)
#     changing_table = db.Column(db.Boolean, nullable=False)
#     directions = db.Column(db.String(200), nullable=True) --- DID NOT INCLUDE THIS 
#     latitude = db.Column(db.Float, nullable=False)
#     longitude = db.Column(db.Float, nullable=False)
#     rating = db.Column(db.Integer, nullable=True)

# @api.post('add-bathroom/<int:bathroom_id>/<string:name>/<string:street>/<string:city>/<string:state>/<string:country>/<string:accessible>/<string:unisex>/<string:changing_table>/<string:latitude>/<string:longitude>/<string:rating>/<string:directions>/<string:comment>')
@api.post('bathrooms/add')
@token_auth.login_required
def addBathroomAPI():
# def addBathroomAPI(bathroom_id, name, street, city, state, country, accessible, unisex, changing_table, 
# latitude, longitude, rating, directions, comment):
    # pass
    # try:
    #     bathroom = Bathroom.query.filter_by(bathroom_id=bathroom_id).first()
    #     print()
    # except:

    data = request.json
    print(data)
    # data = data['bathroom'] # try this 
    id = data['id']
    name = data['name']
    street = data['street']
    city = data['city']
    state = data['state']
    country = data['country']
    accessible = data['accessible']
    unisex = data['unisex']
    changing_table = data['changing_table']
    latitude = data['latitude']
    longitude = data['longitude']
    rating = (data['upvote'] /(data['upvote']  + data['downvote'])) * 5
    directions = data['directions']
    comment = data['comment']

    bathroom_in_db = Bathroom.query.get(id)
    if bathroom_in_db:
        return {
            'status' : 'not ok',
            'message' : 'That bathroom is already in the database.'
        }
    else:
        bathroom = Bathroom(id, name, street, city, state, country, accessible, unisex, changing_table, latitude, longitude, rating, directions, comment)
        bathroom.save_to_db()
        # name, street, city, state, country, accessible, unisex, 
        # changing_table, latitude, longitude, rating

        # user = User(email, password)

        # user.save_to_db()
        return {
            'status' : 'ok',
            'message' : 'Successfully added bathroom to the database.',
            'bathroom' : bathroom.to_dict()
        }
        
