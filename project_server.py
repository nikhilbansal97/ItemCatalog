from flask import Flask, render_template, url_for, request, jsonify, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Character, Movie

app = Flask(__name__)

engine = create_engine('sqlite:///marveldatabase.db')
Base.metadata.bind = engine

Session = sessionmaker(bind = engine)
session = Session()


@app.route('/')
@app.route('/marvels/movies', methods = ['GET', 'POST'])
def showMovies():
	moviesList = session.query(Movie).all()
	return render_template('index.html', moviesList = moviesList)

@app.route('/marvels/movies/new', methods = ['GET','POST'])
def newMovie():
	if request.method == "post":
		
	else
		return render_template('newForm.html', new = 'movie')


@app.route('/marvels/heroes/new', methods = ['GET', 'POST'])
def newHero():
	if request.method == "post":

	else:
		return render_template('newForm.html', new = 'hero')

if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0', port=5000)