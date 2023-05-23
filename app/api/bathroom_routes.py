from . import api
from flask import request
import requests
# we will import some Models here and Authorize the user first. BUT

@api.get('testing')
def testing():
    print('success')
    return {
        'status' : 'ok'
    }

@api.get('search-around-loc/<string:lat>/<string:lng>')
def getBathroomsAroundLoc(lat, lng):
    # NOTE HOW THIS IS JUST ONE PAGE'S WORTH RIGHT NOW... WE WILL HAVE TO CONTINUE THIS WITH MULTIPLE PAGES AND ALSO PASS THAT IN 
    url = f"https://www.refugerestrooms.org/api/v1/restrooms/by_location?page=1&per_page=10&offset=0&lat={lat}&lng={lng}"
    
    response = requests.get(url)
    # if not response.ok:
    #         #return render_template('search.html', form = SignUpForm())
    #         return "Try again?"
    data = response.json()

    print(data)
    return {
        'status' : 'ok',
        'results' : data,
    }

    # const options = {
    #     // mode: 'no-cors',
    #     method: "GET",
    #     headers: {
    #         "Content-Type": 'application/json'
    #     }
    # };