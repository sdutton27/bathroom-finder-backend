from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
from secrets import token_hex # this returns a random hex string in hexadecimal


db = SQLAlchemy()

# this name is actually lowercase
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=True)
    last_name = db.Column(db.String(45), nullable=True)
    email = db.Column(db.String(100), nullable=False) # removed the unique=True in case a user has a Google account and a regular account
    password = db.Column(db.String, nullable=True) # nullable True in case a user is a Google user! This is handled on the front end
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    profile_pic = db.Column(db.String, nullable=True)
    bio = db.Column(db.String(100), nullable=True)
    apitoken = db.Column(db.String, nullable = False, unique=True)
    # account_type = db.Column(db.String(15), nullable=True) # holds if the account is a google account
    google_id = db.Column(db.String(100), nullable=True)

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

    # added this for JSON
    def to_dict(self):
        return {
            'id' : self.user_id,
            'first_name' : self.first_name,
            'last_name' : self.last_name,
            'email' : self.email, 
            'date_created' : self.date_created,
            'profile_pic': self.profile_pic,
            'bio': self.bio,
            'apitoken' : self.apitoken, # we have to have this in here
            'google_id' : self.google_id,
        }