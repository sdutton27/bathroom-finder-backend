from . import api
from ..models import User
from flask import request
from werkzeug.security import check_password_hash
from ..apiauthhelper import basic_auth

@api.post('/signup')
def signUpAPI():
    """
        To create a new user, we are expecting JSON to be formatted like so:
        {       
            "email" : "<properly-formatted-email@email.com>",
            "password" : "<password>"
        }
    """
    data = request.json
    # first_name = data['first_name']
    # last_name = data['last_name']
    # username = data['username']
    email = data['email']
    password = data['password']
    
    user = User.query.filter_by(email=email).first()
    # if user with that email exists
    if user:
        return {
            'status' : 'not ok',
            'message' : 'That email is already in use. Please choose a different email.'
        }, 400
    
    user = User(email, password)

    user.save_to_db()

    return {
        'status' : 'ok',
        'message' : 'You have successfully created an account.',
        'data': user.to_dict()
    }, 201 # successfully created something

@api.post('/login')
@basic_auth.login_required
def loginAPI():

    # data = request.json
    # username = data['username']
    # password = data['password']

    # user = User.query.filter_by(username = username).first()

    # if user:
    #     # that username exists, let's check the password
    #     if check_password_hash(user.password, password):
    #         # if valid, give them their token
            
    return {
        'status':'ok',
        'message':'You have successfully logged in.',
        'data': basic_auth.current_user().to_dict()
    }, 200
    
    #     else: # wrong password
    #         return {
    #             'status':'not ok',
    #             'message':'Incorrect password.',
    #         }, 400
    # else: # username does not exist
    #     return {
    #         'status':'not ok',
    #         'message':'A user with that username does not exist.',
    #     }, 400

@api.post('/google-auth')
def googleLoginAPI():
    data = request.json
    google_id = data['google_id']
    email = data['email']
    profile_pic = data['profile_pic']
    apitoken = data['apitoken']
    
    user = User.query.filter_by(google_id=google_id).first()
    # if user with that email exists
    if user:
        return {
            'status' : 'ok',
            'message' : 'You have successfully signed back into your account.',
            'data' : user.to_dict()

        }, 201
    
    # user = User(email, password)
    user = User(email)

    user.apitoken = apitoken
    user.google_id = google_id
    user.profile_pic = profile_pic

    user.save_to_db()

    return {
        'status' : 'ok',
        'message' : 'You have successfully created an account.',
        'data': user.to_dict()
    }, 201 # successfully created something

