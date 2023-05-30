from . import api
from flask import request
import requests
import os

import base64

from ..apiauthhelper import token_auth

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

@api.get('google-places/<string:loc_search>')
@token_auth.login_required
def getPlacesData(loc_search):
    user = token_auth.current_user() 
    if user:
        # https://maps.googleapis.com/maps/api/place/details/json?place_id=ChIJrTLr-GyuEmsRBfy61i59si0&key=YOUR_API_KEY
        url = f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={loc_search}&inputtype=textquery&fields=formatted_address%2Cname%2Crating%2Cphoto%2Cplace_id&key={GOOGLE_API_KEY}'

        response = requests.get(url)
        data = response.json()

        # print(data)

        if data['status'] == 'OK':
            return {
                'status' : 'ok',
                'data' : data
            }
        else:
            return {
                'status' : 'not ok',
                'response' : 'Unable to locate this Place on Google Places'
            }
    else:
        return {
                'status' : 'not ok',
                'response' : 'That user does not exist.'
            }

@api.get('google-places-photo/<string:photo_reference>')
@token_auth.login_required
def getPlacesPhoto(photo_reference):
    user = token_auth.current_user()
    if user:

        url = f'https://maps.googleapis.com/maps/api/place/photo?maxwidth=200&maxheight=100&photo_reference={photo_reference}&key={GOOGLE_API_KEY}'
        response = requests.get(url, stream=True)
        
        data = response.raw.data
        # data = response.blob()

        # print(data)
        # print(type(data))

        new_data = base64.b64encode(data).decode('ASCII')
        # print(new_data)

        return {
            'status' : 'ok',
            'base_64_image' : new_data
        }
        # return response
    else:
        return {
                'status' : 'not ok',
                'response' : 'That user does not exist.'
            }
