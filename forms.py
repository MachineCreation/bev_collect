from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    first_name = StringField('First name')
    last_name = StringField('First name')
    favorite_liquor = StringField('favorite liquor')
    submit_button = SubmitField()