import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class Catalog(Base):
    __tablename__ = 'catalog'
   
    id = Column(Integer, primary_key=True)
    category = Column(String(60), nullable=False)
    name = Column(String(60), nullable=False)
    description = Column(String(250))
 
    @property
    def serialize(self):
       '''returns data object in JSON format for menu API end points''' 
       return {
           'id':            self.id,
           'category':      self.category,
           'name':          self.name,
           'description':   self.description,
       }

engine = create_engine('sqlite:///catalog.db')
 

Base.metadata.create_all(engine)