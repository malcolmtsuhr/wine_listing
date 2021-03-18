from datetime import datetime
from flask_wtf import Form, FlaskForm
from wtforms import (
    StringField, SelectField, SelectMultipleField, DateTimeField,
    BooleanField, IntegerField, FormField, DecimalField)
from wtforms.validators import (
    DataRequired, AnyOf, URL, InputRequired, Length,
    ValidationError, NoneOf, NumberRange, Regexp)
#from models import *

#type_choices = [(type.id, type.type) for type in Type.query.order_by('id').all()]

type_choices = [
    ('1', 'Red'),
    ('2', 'White'),
    ('3', 'Rose'),
    ('4', 'Sparkling'),
    ('5', 'Dessert')
]

varietal_choices = [
    ('Cabernet Sauvignon', 'Cabernet Sauvignon'),
    ('Syrah', 'Syrah'),
    ('Zinfandel', 'Zinfandel'),
    ('Pinot Noir', 'Pinot Noir'),
    ('Chardonnay', 'Chardonnay'),
    ('Sauvignon Blanc', 'Sauvignon Blanc'),
    ('Pinot Gris', 'Pinot Gris'),
    ('Riesling', 'Riesling'),
    ('other', 'other')
]

country_choices = [
    ('Italy', 'Italy'),
    ('France', 'France'),
    ('Spain', 'Spain'),
    ('United States', 'United States'),
    ('Australia', 'Australia'),
    ('Argentina', 'Argentina'),
    ('China', 'China'),
    ('South Africa', 'South Africa'),
    ('Chile', 'Chile'),
    ('Germany', 'Germany'),
    ('Portugal', 'Portugal'),
    ('Russia', 'Russia'),
    ('Romania', 'Romania'),
    ('Brazil', 'Brazil'),
    ('Hungary', 'Hungary'),
    ('New Zealand', 'New Zealand'),
    ('Greece', 'Greece'),
    ('Austria', 'Austria'),
    ('Ukraine', 'Ukraine'),
    ('Moldova', 'Moldova'),
    ('Bulgaria', 'Bulgaria'),
    ('Serbia', 'Serbia'),
    ('Georgia', 'Georgia'),
    ('Japan', 'Japan'),
    ('Switzerland', 'Switzerland'),
    ('Peru', 'Peru'),
    ('Croatia', 'Croatia'),
    ('Uruguay', 'Uruguay'),
    ('Czech Republic', 'Czech Republic'),
    ('Turkey', 'Turkey'),
    ('Canada', 'Canada'),
    ('Algeria', 'Algeria'),
    ('Slovenia', 'Slovenia'),
    ('Turkmenistan', 'Turkmenistan'),
    ('Mexico', 'Mexico'),
    ('Uzbekistan', 'Uzbekistan'),
    ('Macedonia', 'Macedonia'),
    ('Morocco', 'Morocco'),
    ('Belarus', 'Belarus'),
    ('Slovakia', 'Slovakia'),
    ('Tunisia', 'Tunisia'),
    ('Kazakhstan', 'Kazakhstan'),
    ('India', 'India'),
    ('Israel', 'Israel'),
    ('Albania', 'Albania'),
    ('Montenegro', 'Montenegro'),
    ('Estonia', 'Estonia'),
    ('Cuba', 'Cuba'),
    ('Cyprus', 'Cyprus'),
    ('Azerbaijan', 'Azerbaijan'),
    ('Lebanon', 'Lebanon'),
    ('Armenia', 'Armenia'),
    ('Luxembourg', 'Luxembourg'),
    ('Bolivia', 'Bolivia'),
    ('Madagascar', 'Madagascar'),
    ('Bosnia And Herzegovina', 'Bosnia And Herzegovina'),
    ('Egypt', 'Egypt'),
    ('Lithuania', 'Lithuania'),
    ('United Kingdom', 'United Kingdom'),
    ('Latvia', 'Latvia'),
    ('Zimbabwe', 'Zimbabwe'),
    ('Malta', 'Malta'),
    ('Kyrgyzstan', 'Kyrgyzstan'),
    ('Paraguay', 'Paraguay'),
    ('Ethiopia', 'Ethiopia'),
    ('Belgium', 'Belgium'),
    ('Panama', 'Panama'),
    ('Tajikistan', 'Tajikistan'),
    ('Syria', 'Syria'),
    ('other', 'other')
]

class VintnerForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    country = SelectField(
        'country', validators=[DataRequired()],
        choices=country_choices
    )
    region = StringField(
        'region', validators=[DataRequired()]
    )
    appellation = StringField(
        'appellation'
    )
    website = StringField(
        'website', validators=[URL()]
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )
    creation_date = DateTimeField(
        'creation_date',
        validators=[DataRequired()],
        default=datetime.today()
    )

class VinoForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    year = IntegerField(
        'year',
        validators=[NumberRange(min=1900, max=2025, message='Insert Number'),
                    DataRequired()]
    )
    type = SelectField(
        'type', validators=[DataRequired()],
        choices=type_choices
    )
    varietal = SelectMultipleField(
        'varietal', validators=[DataRequired()],
        choices=varietal_choices
    )
    style = StringField(
        'style', validators=[DataRequired()]
    )
    abv = DecimalField(
        'abv',
        validators=[NumberRange(min=0, max=50, message='Insert Number'),
                    DataRequired()]
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )
    creation_date = DateTimeField(
        'creation_date',
        validators=[DataRequired()],
        default=datetime.today()
    )
    vintner_id = StringField(
        'vintner_id',
        validators=[DataRequired()]
    )
