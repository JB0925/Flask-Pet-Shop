import re
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length, Optional, NumberRange, URL, AnyOf

class AddPetForm(FlaskForm):
    """Form used to create a new pet and add it to the database."""
    name = StringField('Pet Name', validators=[InputRequired(), Length(min=3, max=20)],
                            render_kw={'placeholder': 'Enter The Pet\'s Name'})
    species = StringField('Type of Animal', validators=[InputRequired(), Length(min=3, max=50), AnyOf(['dog', 'cat', 'porcupine'])],
                            render_kw={'placeholder': 'Enter the Type of Animal'})
    photo_url = StringField('Photo URL - optional', validators=[Optional(), URL(require_tld=True)],
                            render_kw={'placeholder': 'Enter a Valid URL'})
    age = IntegerField('Enter the Pet\'s Age - optional', validators=[Optional(), NumberRange(min=0, max=30)],
                            render_kw={'placeholder': 'Enter The Pet\'s Age'})
    notes = TextAreaField('Enter Any Notes - optional', validators=[Optional()],
                            render_kw={'placeholder': 'Enter Any Notes About the Animal Here'})


class EditPetForm(FlaskForm):
    """Form used to edit an existing pet's information, 
       which is then saved to the database."""
    photo_url = StringField('Photo URL - optional', validators=[Optional(), URL(require_tld=True)],
                            render_kw={'placeholder': 'Enter a Valid URL'})
    notes = TextAreaField('Enter Any Notes - optional', validators=[Optional()],
                            render_kw={'placeholder': 'Enter Any Notes About the Animal Here'})
    available = SelectField('Availability', validators=[Optional()], choices=[('true', 'Available'), ('false', 'Not Available')])