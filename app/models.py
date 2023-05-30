from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
from secrets import token_hex # this returns a random hex string in hexadecimal


db = SQLAlchemy()

# JOIN TABLES: 
favorite = db.Table('favorite',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('bathroom_id', db.Integer, db.ForeignKey('bathroom.id'), primary_key=True)
)

# bathroom_waypoint = db.Table('bathroom_waypoint',
#     db.Column('bathroom_id', db.Integer, db.ForeignKey('bathroom.id'), primary_key=True),
#     db.Column('directions_id', db.Integer, db.ForeignKey('directions.directions_id'), primary_key=True)
# )


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
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(45), nullable=False)
    state = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(15), nullable=False)
    accessible = db.Column(db.Boolean, nullable=False)
    unisex = db.Column(db.Boolean, nullable=False)
    changing_table = db.Column(db.Boolean, nullable=False)
    comment = db.Column(db.String, nullable=True)
    directions = db.Column(db.String, nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Integer, nullable=True)

    # join table for Favorites
    favoriters = db.relationship('User', secondary = 'favorite', overlaps="favorited")
    
    # join table for Bathroom Waypoint 
    # on_route = db.relationship('Directions', secondary='bathroom_waypoint', lazy = True)

    # join table for RecentSearch
    # searched_locs = db.relationship('RecentSearch', secondary='searched_bathroom', overlaps="searched_bathrooms", lazy = True)
    
    
    recent_searches = db.relationship("RecentSearch", secondary="searched_bathroom",
                                      back_populates="bathrooms", viewonly = True)
    
    searched_locs = db.relationship("SearchedBathroom", back_populates="bathroom")
    # recent_searches = db.relationship("RecentSearch", secondary="searched_bathroom", back_populates="bathrooms")


    def __init__(self, id, name, street, city, state, country, accessible, unisex, 
                 changing_table, latitude, longitude, rating, directions, comment):
        self.id = id
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
        self.comment = comment

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
            'id':self.id,
            'name': self.name,
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'accessible': self.accessible,
            'unisex': self.unisex,
            'changing_table': self.changing_table,
            'directions': self.directions,
            'comment' : self.comment,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'rating': self.rating
            
        }
    
# class Directions(db.Model):
#     directions_id = db.Column(db.Integer, primary_key=True)
#     origin = db.Column(db.String(100), nullable=False)
#     destination = db.Column(db.String(100), nullable=True) # This can be null if the user just searches for bathrooms around 1 location

#     # join table for Bathroom Waypoints
#     waypoints = db.relationship('Bathroom', secondary = 'bathroom_waypoint', overlaps="on_route")

#     def __init__(self, origin, destination=""):
#         self.origin = origin
#         self.destination = destination

#     def save_to_db(self):
#         db.session.add(self)
#         db.session.commit() 

#     def delete_from_db(self):
#         db.session.delete(self)
#         db.session.commit()

#     def save_changes_to_db(self):
#         db.session.commit()

#     def add_waypoint(self, bathroom):
#         self.waypoints.append(bathroom)
#         db.session.commit()
    
#     def remove_waypoint(self, bathroom):
#         self.waypoints.remove(bathroom)
#         db.session.commit()
    
#     def waypoints_to_dict(self):
#         waypoints_dict = {}
#         counter = 1
#         for bathroom in self.waypoints:
#             waypoints_dict[counter] = bathroom.to_dict()
#             counter += 1
#         return {
#             'origin' : self.origin,
#             'destination' : self.destination,
#             'bathroom_waypoints': waypoints_dict
#         }

#     def to_dict(self):
#         return {
#             'directions_id' : self.directions_id,
#             'origin': self.origin,
#             'destination' : self.destination
#         } 
    
# class RecentSearch(db.Model):
#     __tablename__ = 'recent_search'
#     search_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable = False)
#     # directions_id = db.Column(db.Integer, db.ForeignKey('directions.directions_id'), nullable = True)
#     bathroom_id = db.Column(db.Integer, db.ForeignKey('bathroom.id'), nullable = True)

#     # make sure that if you are making a user<->bathroom, that you still put bathroom after "" for directions_id
#     def __init__(self, user_id, bathroom_id=""):
#         self.user_id = user_id
#         # self.directions_id = directions_id
#         self.bathroom_id = bathroom_id

#     def save_to_db(self):
#         db.session.add(self)
#         db.session.commit() 

#     def delete_from_db(self):
#         db.session.delete(self)
#         db.session.commit()

#     def save_changes_to_db(self):
#         db.session.commit()

#     def to_dict(self):
#         if self.bathroom_id:
#             return {
#                 'user_id' : self.user_id,
#                 'bathroom_id' : self.bathroom_id
#             }
#         # else:
#         #     return {
#         #         'user_id' : self.user_id,
#         #         'directions_id' : self.directions_id
#         #     }

class RecentSearch(db.Model):
    search_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable = False)
    time_searched = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    origin = db.Column(db.String(250), nullable=False)
    destination = db.Column(db.String(250), nullable=True)

    # TABLE:

    #

    # Paris, France - 9:00PM
    #     - Target 9:01PM
    #     - Starbucks 9:00:45PM
    #     - Antoher Bathroom 9:00:30PM
    # Berlin, Germany  - 8:00PM
    #     - Another Bathroom - 8:01PM

    # searched_bathrooms = db.relationship('Bathroom', secondary='searched_bathroom')
    
    
    bathrooms = db.relationship("Bathroom", secondary = "searched_bathroom",
                                back_populates= "recent_searches", viewonly=True)
    searched_bathrooms = db.relationship("SearchedBathroom", back_populates="recent_search")
    # bathrooms = db.relationship("Bathroom", secondary="searched_bathroom", back_populates= "recent_searches")

    def __init__(self, user_id, origin, destination=""):
        self.user_id = user_id
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

    def add_searched_bathroom(self, bathroom_id):
        #self.searched_bathrooms.append(bathroom_id)
        bathroom = SearchedBathroom(self.search_id, bathroom_id)
        db.session.add(bathroom)
        self.searched_bathrooms.append(bathroom)
        # self.bathrooms.append(SearchedBathroom(self.search_id, bathroom_id))
        db.session.commit()

    def remove_searched_bathroom(self, bathroom_id):
        # self.searched_bathrooms.remove(bathroom_id)
        # not sure if this works
        # self.searched_bathrooms.remove(SearchedBathroom.query.filter_by(bathroom_id = bathroom_id, search_id = self.search_id).first())
        bathroom = SearchedBathroom.query.filter_by(bathroom_id = bathroom_id, search_id = self.search_id).first()
        db.session.delete(bathroom)    
        # self.searched_bathrooms.delete().where(self.searched_bathrooms.c.bathroom_id == bathroom_id)
        db.session.commit()

    def to_dict(self):
        return {
            'search_id' : self.search_id,
            'user_id' : self.user_id,
            'time_searched' : self.time_searched,
            'origin' : self.origin,
            'destination' : self.destination
        }
    def searched_bathrooms_to_list(self):
        bathrooms_list = []
        for bathroom in self.searched_bathrooms:
            # print(bathroom_id)
            # searched_bathroom = SearchedBathroom.query.filter_by(bathroom_id = bathroom_id).first()
            # print(searched_bathroom)
            bathrooms_list.append(bathroom.to_dict())
        return bathrooms_list
        # return {
        #     'directions_id' : self.directions_id,
        #     'origin': self.origin,
        #     'destination' : self.destination
        # } 

class SearchedBathroom(db.Model):
    __tablename__ = 'searched_bathroom'
    
    searched_bathroom_id = db.Column(db.Integer, primary_key=True)
    search_id = db.Column(db.Integer, db.ForeignKey('recent_search.search_id'), nullable = False)
    bathroom_id = db.Column(db.Integer, db.ForeignKey('bathroom.id'), nullable = False)
    time_searched = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)

    recent_search = db.relationship("RecentSearch", back_populates="searched_bathrooms")
    bathroom = db.relationship("Bathroom", back_populates="searched_locs")
    # recent_search = db.relationship("RecentSearch", backref=db.backref("searched_bathroom"), viewonly=True)
    # bathroom = db.relationship("Bathroom", backref=db.backref("searched_bathroom"), viewonly=True)

    def __init__(self, search_id, bathroom_id):
        self.search_id = search_id
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
        return {
            "searched_bathroom_id" : self.searched_bathroom_id,
            "search_id" : self.search_id,
            "bathroom_id" : self.bathroom_id,
            "time_searched" : self.time_searched
        }