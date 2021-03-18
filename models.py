import os
from flask import (
    Flask, render_template, request, Response, flash, redirect, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form, FlaskForm
import json
import sys
import logging
from logging import Formatter, FileHandler
from flask_migrate import Migrate
from flask_moment import Moment
from datetime import datetime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import (
    Table, Column, String, Integer, Numeric, DateTime, create_engine, ForeignKey)
from sqlalchemy.dialects.postgresql import ARRAY

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

'''
Vintner
Wine maker & region details
'''
class Vintner(db.Model):

    __tablename__ = 'vintners'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    area_id = Column(Integer, ForeignKey('areas.id'))
    website = Column(String)
    image_link = Column(String)
    creation_date = Column(DateTime, nullable=False)
    wines = relationship('Vino', backref='vintners',
                        cascade='all, delete-orphan', lazy='joined')

    def __init__(self, name, area_id, website, image_link, creation_date):
        self.name = name
        self.area_id = area_id
        self.website = website
        self.image_link = image_link
        self.creation_date = creation_date

    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'area_id': self.area_id,
          'website': self.website,
          'image_link': self.image_link,
          'creation_date': self.creation_date
        }


'''
Vino
Wine & desciption details
'''
class Vino(db.Model):
    __tablename__ = 'wines'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    year = Column(Integer)
    type_id = Column(Integer, ForeignKey('types.id'))
    varietal = Column(ARRAY(String), nullable=False)
    style = Column(String)
    abv = Column(Numeric(precision=4, scale=2))
    image_link = Column(String)
    creation_date = Column(DateTime, nullable=False)
    vintner_id = Column(Integer, ForeignKey('vintners.id'))

    def __init__(self, name, year, type_id,
          varietal, style, abv, image_link, creation_date, vintner_id):
        self.name = name
        self.year = year
        self.type_id = type_id
        self.varietal = varietal
        self.style = style
        self.abv = abv
        self.image_link = image_link
        self.creation_date = creation_date
        self.vintner_id = vintner_id

    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'year': self.year,
          'type_id': self.type_id,
          'varietal': self.varietal,
          'style': self.style,
          'abv': self.abv,
          'image_link': self.image_link,
          'creation_date': self.creation_date,
          'vintner_id': self.vintner_id
        }


'''
Area
Country, Region, and Local Appellation combo
'''
class Area(db.Model):
    __tablename__ = 'areas'

    id = Column(Integer, primary_key=True)
    country = Column(String)
    region = Column(String)
    appellation = Column(String)
    vintners = relationship('Vintner', backref='areas',
                        cascade='all, delete-orphan', lazy='joined')

    def __init__(self, id, country, region, appellation):
        self.id = id
        self.country = country
        self.region = region
        self.appellation = appellation

    def format(self):
        return {
          'id': self.id,
          'country': self.country,
          'region': self.region,
          'appellation': self.appellation,
        }


'''
Type
Vino type category associated & description
'''
class Type(db.Model):
    __tablename__ = 'types'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    description = Column(String)
    wines = relationship('Vino', backref='types',
                        cascade='all, delete-orphan', lazy='joined')

    def __init__(self, id, type, description):
        self.id = id
        self.type = type
        self.description = description

    def format(self):
        return {
          'id': self.id,
          'type': self.type,
          'description': self.description
        }
