import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Users(Base):
    __tablename__ = 'user'
    
    id = Column(String(25), primary_key=True)
    password = Column(String(15), nullable=False)


class Episodes(Base):
    __tablename__ = 'episode'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    name = Column(String(25), nullable=False)
    user_name = Column(Integer, ForeignKey('user.id'))
    private = Column(Boolean, nullable=False)
    latitude = Column(Float , nullable=False)
    longitude = Column(Float, nullable=False)
    description = Column(String(250))
    geohash = Column(String(250), nullable=False)
    filename = Column(String(250))
    user = relationship(Users)


    __mapper_args__ = {"order_by":geohash}

    @property
    def serializeEpisode(self):
        #Returns object data in easily serializable format
        return {'id' : self.id, 'timestamp ' : self.timestamp,
        'name' : self.name, 'username' : self.user_name, 'private' : self.private, 'latitude' : self.latitude, 'longitude' : self.longitude, 
       'description' : self.description, 'geohash' : self.geohash, 'filename' : self.filename }    

class Photos(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True)
    episode_id = Column(Integer, ForeignKey('episode.id'))
    filename = Column(String(250), nullable=False)
    description = Column(String(250))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    geohash = Column(String(250), nullable=False)
    episode = relationship(Episodes)

    __mapper_args__ = {"order_by":geohash}

    @property
    def serializePhoto(self):
        #Returns object data in easily serializable format
        return {'id' : self.id,'description' : self.description, 'episode_id' : self.episode_id, 'filename' : self.filename,
        'latitude' : self.latitude, 'longitude' : self.longitude, 'geohash' : self.geohash}




engine = create_engine('sqlite:///hoodly.db')


Base.metadata.create_all(engine)
