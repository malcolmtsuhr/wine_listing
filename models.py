from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

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


'''
Vintner
Wine maker & region details
'''
class Vintner(db.Model):
  __tablename__ = 'vintners'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  country = Column(String)
  region = Column(String)
  appellation = Column(String)
  wines = relationship('Question', backref='wines',
                             cascade='all, delete-orphan', lazy='joined')

  def __init__(self, name, region):
    self.name = name
    self.region = region

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'country': self.country,
      'region': self.region,
      'appellation': self.appellation
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
  type = Column(String)
  varietal = Column(String)
  style = Column(String)
  grape = Column(String)
  abv = Column(Integer)
  image_link = Column(String)
  vintner = Column(Integer, ForeignKey('vintners.id'))

  def __init__(self, name, region):
    self.name = name
    self.year = year
    self.type = type
    self.varietal = varietal
    self.style = style
    self.grape = grape
    self.abv = abv
    self.image_link = image_link
    self.vintner = vintner

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'year': self.year,
      'type': self.type,
      'varietal': self.varietal,
      'style': self.style,
      'grape': self.grape,
      'abv': self.abv,
      'image_link': self.image_link,
      'vintner': self.vintner
    }
