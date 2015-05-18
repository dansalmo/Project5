import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class User(Base):
    __tablename__ = 'user'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

class Catalog(Base):
    __tablename__ = 'catalog'
   
    id = Column(Integer, primary_key=True)
    category = Column(String(60), nullable=False)
    name = Column(String(60), nullable=False)
    description = Column(String(250))
    imageURL = Column(String(500))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
 
    @property
    def serialize(self):
       '''returns data object in JSON format for menu API end points''' 
       return {
           'id':            self.id,
           'category':      self.category,
           'name':          self.name,
           'description':   self.description,
           'imageURL':      self.imageURL
       }

#engine = create_engine('sqlite:///catalog.db')
engine = create_engine('postgresql+psycopg2://catalog:hu8jmn3@localhost/catalog')

Base.metadata.create_all(engine)