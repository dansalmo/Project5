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

    @property
    def serializeXML(self):
       '''returns data object in JSON format for menu API end points''' 
       import xml.etree.ElementTree as ET
       root = ET.element('root')  # name the root whatever you want
       # add your data to the root node in the format you want
       return ET.dump(root)

engine = create_engine('sqlite:///catalog.db')
 

Base.metadata.create_all(engine)