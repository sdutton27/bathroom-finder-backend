from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
from secrets import token_hex # this returns a random hex string in hexadecimal


db = SQLAlchemy()

# JOIN TABLES: 
favorite = db.Table('favorite',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('bathroom_id', db.Integer, db.ForeignKey('bathroom.bathroom_id'), primary_key=True)
)

bathroom_waypoint = db.Table('bathroom_waypoint',
    db.Column('bathroom_id', db.Integer, db.ForeignKey('bathroom.bathroom_id'), primary_key=True),
    db.Column('directions_id', db.Integer, db.ForeignKey('directions.directions_id'), primary_key=True)
)


# this name is actually lowercase
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=True)
    last_name = db.Column(db.String(45), nullable=True)
    pronouns = db.Column(db.String(10), nullable=True)
    email = db.Column(db.String(100), nullable=False) # removed the unique=True in case a user has a Google account and a regular account
    password = db.Column(db.String, nullable=True) # nullable True in case a user is a Google user! This is handled on the front end
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    profile_pic = db.Column(db.String, nullable=True)
    bio = db.Column(db.String(100), nullable=True)
    apitoken = db.Column(db.String, nullable = False, unique=True)
    # account_type = db.Column(db.String(15), nullable=True) # holds if the account is a google account
    google_id = db.Column(db.String(100), nullable=True)

    # join table 
    favorited = db.relationship('Bathroom', secondary='favorite', cascade="all, delete", lazy = True)

    def __init__(self, email, password=""):
        self.email = email
        self.password = generate_password_hash(password)
        self.apitoken = token_hex(16)

    # def change_user_id(self, new_uid):
    #     self.user_id = new_uid
    #     db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit() # actually commits things

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_changes_to_db(self):
        db.session.commit()

    def favorite(self, bathroom):
        self.favorited.append(bathroom)
        db.session.commit()
    
    def unfavorite(self, bathroom):
        self.favorited.remove(bathroom)
        db.session.commit()
    
    # def favorites_to_dict(self):
    #     faves_dict = {}
    #     counter = 1
    #     for bathroom in self.favorited:
    #         faves_dict[counter] = bathroom.to_dict()
    #         counter += 1
    #     return {'favorites': faves_dict}
    
    def favorites_to_list(self):
        faves_list = []
        for bathroom in self.favorited:
            faves_list.append(bathroom.to_dict())
        return faves_list

    # added this for JSON
    def to_dict(self):
        return {
            'id' : self.user_id,
            'first_name' : self.first_name,
            'last_name' : self.last_name,
            'pronouns' : self.pronouns,
            'email' : self.email, 
            'date_created' : self.date_created,
            'profile_pic': self.profile_pic,
            'bio': self.bio,
            'apitoken' : self.apitoken, # we have to have this in here
            'google_id' : self.google_id,
        }

class Bathroom(db.Model):
    bathroom_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(45), nullable=False)
    street = db.Column(db.String(45), nullable=False)
    city = db.Column(db.String(45), nullable=False)
    state = db.Column(db.String(2), nullable=True)
    country = db.Column(db.String(15), nullable=False)
    accessible = db.Column(db.Boolean, nullable=False)
    unisex = db.Column(db.Boolean, nullable=False)
    changing_table = db.Column(db.Boolean, nullable=False)
    directions = db.Column(db.String(200), nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Integer, nullable=True)

    # join table for Favorites
    favoriters = db.relationship('User', secondary = 'favorite', overlaps="favorited")
    
    # join table for Bathroom Waypoint 
    on_route = db.relationship('Directions', secondary='bathroom_waypoint', lazy = True)

    def __init__(self, name, street, city, state, country, accessible, unisex, 
                 changing_table, directions, latitude, longitude, rating):
        self.name = name
        self.street = street 
        self.city = city
        self.state = state
        self.country = country
        self.accessible = accessible
        self.unisex = unisex
        self.changing_table = changing_table
        self.directions = directions 
        self.latitude = latitude
        self.longitude = longitude
        self.rating = rating

    def save_to_db(self):
        db.session.add(self)
        db.session.commit() 

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_changes_to_db(self):
        db.session.commit()

    def to_dict(self):
        return {
            'id':self.bathroom_id,
            'name': self.name,
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'accessible': self.accessible,
            'unisex': self.unisex,
            'changing_table': self.changing_table,
            'directions': self.directions,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'rating': self.rating
        }
    
class Directions(db.Model):
    directions_id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=True) # This can be null if the user just searches for bathrooms around 1 location

    # join table for Bathroom Waypoints
    waypoints = db.relationship('Bathroom', secondary = 'bathroom_waypoint', overlaps="on_route")

    def __init__(self, origin, destination=""):
        self.origin = origin
        self.destination = destination

    def save_to_db(self):
        db.session.add(self)
        db.session.commit() 

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_changes_to_db(self):
        db.session.commit()

    def add_waypoint(self, bathroom):
        self.waypoints.append(bathroom)
        db.session.commit()
    
    def remove_waypoint(self, bathroom):
        self.waypoints.remove(bathroom)
        db.session.commit()
    
    def waypoints_to_dict(self):
        waypoints_dict = {}
        counter = 1
        for bathroom in self.waypoints:
            waypoints_dict[counter] = bathroom.to_dict()
            counter += 1
        return {
            'origin' : self.origin,
            'destination' : self.destination,
            'bathroom_waypoints': waypoints_dict
        }

    def to_dict(self):
        return {
            'directions_id' : self.directions_id,
            'origin': self.origin,
            'destination' : self.destination
        } 
    
class RecentSearch(db.Model):
    __tablename__ = 'recent_search'
    search_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable = False)
    directions_id = db.Column(db.Integer, db.ForeignKey('directions.directions_id'), nullable = True)
    bathroom_id = db.Column(db.Integer, db.ForeignKey('bathroom.bathroom_id'), nullable = True)

    # make sure that if you are making a user<->bathroom, that you still put bathroom after "" for directions_id
    def __init__(self, user_id, directions_id="", bathroom_id=""):
        self.user_id = user_id
        self.directions_id = directions_id
        self.bathroom_id = bathroom_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit() 

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_changes_to_db(self):
        db.session.commit()

    def to_dict(self):
        if self.bathroom_id:
            return {
                'user_id' : self.user_id,
                'bathroom_id' : self.bathroom_id
            }
        else:
            return {
                'user_id' : self.user_id,
                'directions_id' : self.directions_id
            }
