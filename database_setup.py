import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# This is the Movie class which is used to make objects of movie.


class Movie(Base):
    # Table name of the Movie class.
    __tablename__ = "movies"

    # Variables that act as columns for the table.
    id = Column(Integer, primary_key=True)
    name = Column(Integer, nullable=False)
    description = Column(String(250), nullable=False)
    image_path = Column(String(100))

    # This method is used to convert the Movie object and return the Object
    # for JSON Response.
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

# This is the Character class which is used to make different Characters.


class Character(Base):
    # The table name of the Character class.
    __tablename__ = "characters"

    # Variables that are used as columns for the table.
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250), nullable=False)
    movie = relationship(Movie)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    image_path = Column(String(100))

    # This method is used to convert the Character object and return the
    # Object for JSON Response
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


# This is the User class that is used for the Users logging in.
class User(Base):
    # The table name for the class.
    __tablename__ = "users"

    # Variables that act as columns for the table.
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    api_key = Column(String(40), nullable=False)

engine = create_engine('sqlite:///marveldatabase.db')
Base.metadata.create_all(engine)
