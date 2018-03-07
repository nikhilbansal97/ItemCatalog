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
	return render_template('index.html', moviesList = moviesList, showContent = "movies")

@app.route('/marvels/heroes', methods = ['GET', 'POST'])
def showHeroes():
	heroesList = session.query(Character).all()
	return render_template('index.html', heroesList = heroesList, showContent = "heroes")

@app.route('/marvels/movies/new', methods = ['GET','POST'])
def newMovie():
	if request.method == 'POST':
		name = request.form['inputName']
		description = request.form['inputDescription']
		link = request.form['inputLink']
		movie = Movie(name = name, description = description, image_path = link)
		session.add(movie)
		session.commit()
		return redirect(url_for('showMovies'))
	else:
		return render_template('newForm.html', new = 'movie')


@app.route('/marvels/heroes/new', methods = ['GET', 'POST'])
def newHero():
	if request.method == 'POST':
		name = request.form['inputName']
		description = request.form['inputDescription']
		link = request.form['inputLink']
		hero = Character(name = name, description = description, image_path = link)
		session.add(hero)
		session.commit()
		return redirect(url_for('showHeroes'))
	else:
		return render_template('newForm.html', new = 'hero')

if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0', port=5000)