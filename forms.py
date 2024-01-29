from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    first_name = StringField('First name', validators = [DataRequired()])
    last_name = StringField('First name', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    favorite_liquor = StringField('favorite liquor', validators= [DataRequired()])
    submit_button = SubmitField()