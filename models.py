from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets

                                                                                # set variables for class instantiation

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

                                                                                # create class for generating user information and storing it in our DB(using SQLAlchemy)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable = False,)
    last_name = db.Column(db.String(150), nullable = False,)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    favorite_liquor = db.Column(db.String, nullable = False)
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, first_name, last_name, favorite_liquor, password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.favorite_liquor = favorite_liquor
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has added to the database'
    
                                                                                # create a class to take in contact info and store it to the phonebook for later Queries DB
    
class Beverage(db.Model):
    id = db.Column(db.String, primary_key = True)
    base_liquor = db.Column(db.String(150), nullable = False)
    name = db.Column(db.String(200), nullable = False)
    glass_type = db.Column(db.String(40), nullable = False)
    recipe = db.Column(db.String(550), nullable = False)
    comments = db.Column(db.String(150), nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, base_liquor, name, glass_type, recipe, comments, user_token, id = ''):
        self.id = self.set_id()
        self.base_liquor = base_liquor
        self.name = name
        self.glass_type = glass_type
        self.recipe = recipe
        self.comments = comments
        self.user_token = user_token


    def __repr__(self):
        return f'The following Recipe has been added to the Beverage Collection:\n Name: {self.name}\n base liquor: {self.base_liquor}\n Glass size: {self.glass_type}'

    def set_id(self):
        return (secrets.token_urlsafe())
    
                                                                                # not quite sure what this is for yet. I'm not familear with Marshmallow

class beverageSchema(ma.Schema):
    class Meta:
        fields = ['id', 'base_liquor','name','glass_type', 'recipe','comments']

beverage_schema = beverageSchema()
beverages_schema = beverageSchema(many=True)