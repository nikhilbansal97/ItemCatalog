import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Movie(Base):
	__tablename__ = "movies"
	id = Column(Integer, primary_key = True)
	name = Column(Integer, nullable = False)
	description = Column(String(250), nullable = False)
	image_path = Column(String(100))

	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'description': self.description
		}

class Character(Base):
	__tablename__ = "characters"
	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	description = Column(String(250), nullable = False)
	movie = relationship(Movie)
	movie_id = Column(Integer, ForeignKey('movies.id'))
	image_path = Column(String(100))

	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'description': self.description
		}


class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	email = Column(String(80), nullable = False)
	api_key = Column(String(40), nullable = False)

engine = create_engine('sqlite:///marveldatabase.db')
Base.metadata.create_all(engine)