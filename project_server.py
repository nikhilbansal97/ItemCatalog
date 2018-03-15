from flask import Flask, render_template, url_for, request, jsonify, redirect
from flask import session as login_session
import random, string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Character, Movie, User
#For signin
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

app = Flask(__name__)

engine = create_engine('sqlite:///marveldatabase.db')
Base.metadata.bind = engine

Session = sessionmaker(bind = engine)
session = Session()

@app.route('/')
@app.route('/marvels/movies', methods = ['GET', 'POST'])
def showMovies():
	moviesList = session.query(Movie).all()
	user = None
	if 'access_token' not in login_session or login_session['access_token'] is None:
		loginStatus = 0
	else:
		loginStatus = 1
		user = session.query(User).filter_by(email = login_session['email']).one()
	return render_template('index.html', moviesList = moviesList, showContent = "movies", loginStatus = loginStatus, user = user)

def getRandomToken():
	api_token = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(16))
	return api_token

@app.route('/marvels/movies/json')
def getMoviesJson():
	queryParams = request.args
	if 'access_token' not in login_session or login_session['access_token'] is None:
		response = make_response(json.dumps('User not Logged in!'), 401)
		response.headers['Content-Type'] = "application/json"
		return response
	if 'api_key' in queryParams and len(queryParams['api_key']) > 0:
		user = session.query(User).filter_by(api_key = queryParams['api_key']).one_or_none()
		if user is None:
			response = make_response(json.dumps('Wrong API Key'), 401)
			response.headers['Content-Type'] = "application/json"
			return response
		else:
			moviesList = session.query(Movie).all()
			return jsonify([movie.serialize for movie in moviesList])
	elif 'api_key' not in queryParams:
		response = make_response(json.dumps('api_key parameter not found'), 401)
		response.headers['Content-Type'] = "application/json"
		return response
	elif len(queryParams['api_key']) == 0:
		response = make_response(json.dumps('No api key found!'), 401)
		response.headers['Content-Type'] = "application/json"
		return response


@app.route('/marvels/characters/json')
def getCharactersJson():
	queryParams = request.args
	if 'access_token' not in login_session or login_session['access_token'] is None:
		response = make_response(json.dumps('User not Logged in!'), 401)
		response.headers['Content-Type'] = "application/json"
		return response
	if 'api_key' in queryParams and len(queryParams['api_key']) > 0:
		user = session.query(User).filter_by(api_key = queryParams['api_key']).one_or_none()
		if user is None:
			response = make_response(json.dumps('Wrong API Key'), 401)
			response.headers['Content-Type'] = "application/json"
			return response
		else:
			characterList = session.query(Character).all()
			return jsonify([character.serialize for character in characterList])
	elif 'api_key' not in queryParams:
		response = make_response(json.dumps('api_key parameter not found'), 401)
		response.headers['Content-Type'] = "application/json"
		return response
	elif len(queryParams['api_key']) == 0:
		response = make_response(json.dumps('No api key found!'), 401)
		response.headers['Content-Type'] = "application/json"
		return response

@app.route('/marvels/characters/<int:id>/json')
def getSpecificCharacterJson(id):
	queryParams = request.args
	if 'access_token' not in login_session or login_session['access_token'] is None:
		response = make_response(json.dumps('User not Logged in!'), 401)
		response.headers['Content-Type'] = "application/json"
		return response
	if 'api_key' in queryParams and len(queryParams['api_key']) > 0:
		user = session.query(User).filter_by(api_key = queryParams['api_key']).one_or_none()
		if user is None:
			response = make_response(json.dumps('Wrong API Key'), 401)
			response.headers['Content-Type'] = "application/json"
			return response
		else:
			character = session.query(Character).filter_by(id = id).one_or_none()
			if character is None:
				response = make_response(json.dumps('No Character Found'), 401)
				response.headers['Content-Type'] = "application/json"
				return response
			return jsonify(character.serialize)
	elif 'api_key' not in queryParams:
		response = make_response(json.dumps('api_key parameter not found'), 401)
		response.headers['Content-Type'] = "application/json"
		return response
	elif len(queryParams['api_key']) == 0:
		response = make_response(json.dumps('No api key found!'), 401)
		response.headers['Content-Type'] = "application/json"
		return response

@app.route('/marvels/movies/<int:id>/json')
def getSpecificMoveiJson(id):
	queryParams = request.args
	if 'access_token' not in login_session or login_session['access_token'] is None:
		response = make_response(json.dumps('User not Logged in!'), 401)
		response.headers['Content-Type'] = "application/json"
		return response
	if 'api_key' in queryParams and len(queryParams['api_key']) > 0:
		user = session.query(User).filter_by(api_key = queryParams['api_key']).one_or_none()
		if user is None:
			response = make_response(json.dumps('Wrong API Key'), 401)
			response.headers['Content-Type'] = "application/json"
			return response
		else:
			movie = session.query(Movie).filter_by(id = id).one_or_none()
			if movie is None:
				response = make_response(json.dumps('No Movie Found'), 401)
				response.headers['Content-Type'] = "application/json"
				return response
			return jsonify(movie.serialize)
	elif 'api_key' not in queryParams:
		response = make_response(json.dumps('api_key parameter not found'), 401)
		response.headers['Content-Type'] = "application/json"
		return response
	elif len(queryParams['api_key']) == 0:
		response = make_response(json.dumps('No api key found!'), 401)
		response.headers['Content-Type'] = "application/json"
		return response

@app.route('/login')
def login():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
	login_session['state'] = state
	return render_template('login.html', STATE = state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid State Parameter'), 401)
		response.headers['Content-Type'] = "application/json"
		return response
	code = request.data
	try:
		# Upgrade the authorization code to credentials object
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope = "")
		oauth_flow.redirect_uri = "postmessage"
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(json.dumps('Failed to upgrade the authorization code.', 401))
		response.headers['Content-Type'] = "application/json"
		return response
	# Check that the acess token is valid
	access_token = credentials.access_token
	url = ("https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s" % access_token)
	h = httplib2.Http()
	resp, content = h.request(url, 'GET')
	result = json.loads(content.decode('utf-8'))
	
	# If there was an error in access token, abort.
	if 'error' in result:
		response = make_request(json.dumps("Token's user ID doesn't match the given user id"), 401)
		response.headers['Content-Type'] = "application/json"
		return response
	# Verify that the access token is used for the intended user
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(json.dumps("Token's user ID doesn't match the user id"), 401)
		response.headers['Content-Type'] = "application/json"
		return response
	if result['issued_to'] != CLIENT_ID:
		response = make_response(json.dumps("Token's client ID doesn't match the app's"), 401)
		print ("Token's client ID doesn't match the app's")
		response.headers['Content-Type'] = "application/json"
		return response
	# Check if user is already logged in.
	stored_credentials = login_session.get('access_token')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_credentials is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps("User is already logged in"), 200)
		response.headers['Content-Type'] = "application/json"
		return response
	# Store the acess token in the login session for later use
	login_session['access_token'] = credentials.access_token
	login_session['gplus_id'] = gplus_id

	# Get user info
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt':'json'}
	answer = requests.get(userinfo_url, params = params)
	data = json.loads(answer.text)

	login_session['username'] = data["name"]
	login_session['picture'] = data["picture"]
	login_session['email'] = data["email"]

	userInfo = session.query(User).filter_by(email = data["email"]).one_or_none()
	if userInfo is None:
		newUser = User(name = data["name"], email = data["email"], api_key = getRandomToken())
		session.add(newUser)
		session.commit()

	output = ''
	output += '<h1>Welcome, '
	output += login_session['username']
	output += '!</h1>'
	output += '<img src="'
	output += login_session['picture']
	output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
	print ("done!")
	return output


@app.route('/gdisconnect')
def gdisconnect():
	if 'access_token' not in login_session or login_session['access_token'] is None:
		return redirect(url_for('showMovies'))
	access_token = login_session.get('access_token')
	if access_token is None:
		response = make_response('Currect user not connected.', 401)
		response.headers['Content-Type'] = "application/json"
		return response
	url = "https://accounts.google.com/o/oauth2/revoke?token=%s" % access_token
	h = httplib2.Http()
	resp, content = h.request(url, 'GET')
	print (content)
	print (resp.get('status'))
	print ("Logged out!")
	login_session['state'] = None
	login_session['access_token'] = None
	return redirect(url_for('showMovies'))

@app.route('/marvels/heroes', methods = ['GET', 'POST'])
def showHeroes():
	heroesList = session.query(Character).all()
	user = None
	if login_session['access_token'] is None:
		loginStatus = 0
	else:
		loginStatus = 1
		user = session.query(User).filter_by(email = login_session['email']).one()
	return render_template('index.html', heroesList = heroesList, showContent = "heroes", loginStatus = loginStatus, user = user)

@app.route('/marvels/movies/new', methods = ['GET','POST'])
def newMovie():
	if 'access_token' not in login_session or login_session['access_token'] is None:
		response = make_response(json.dumps('User not Logged in!'), 401)
		response.headers['Content-Type'] = "application/json"
		return response
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

@app.route('/marvels/movies/<int:movie_id>/edit', methods = ['GET', 'POST'])
def editMovie(movie_id):
	if 'access_token' not in login_session or login_session['access_token'] is None:
		response = make_response(json.dumps('User not Logged in!'), 401)
		response.headers['Content-Type'] = "application/json"
		return response
	movie = session.query(Movie).filter_by(id = movie_id).one()
	if request.method == 'POST':
		movie.name = request.form['inputName']
		movie.description = request.form['inputDescription']
		movie.image_path = request.form['inputLink']
		session.add(movie)
		session.commit()
		return redirect(url_for('showMovies'))
	return render_template('editForm.html', movie = movie, edit = "movie")

@app.route('/marvel/heros/<int:hero_id>/edit', methods = ['GET', 'POST'])
def editHero(hero_id):
	if 'access_token' not in login_session or login_session['access_token'] is None:
		response = make_response(json.dumps('User not Logged in!'), 401)
		response.headers['Content-Type'] = "application/json"
		return response
	hero = session.query(Character).filter_by(id = hero_id).one()
	if request.method == 'POST':
		hero.name = request.form['inputName']
		hero.description = request.form['inputDescription']
		hero.image_path = request.form['inputLink']
		session.add(hero)
		session.commit()
		return redirect(url_for('showHeroes'))
	return render_template('editForm.html', hero = hero, edit = "hero")

@app.route('/marvel/heros/<int:hero_id>/delete', methods = ['POST'])
def deleteHero(hero_id):
	if 'access_token' not in login_session or login_session['access_token'] is None:
		response = make_response(json.dumps('User not Logged in!'), 401)
		response.headers['Content-Type'] = "application/json"
		return response
	hero = session.query(Character).filter_by(id = hero_id).one()
	if request.method == 'POST':
		session.delete(hero)
		session.commit()
		return redirect(url_for('showHeroes'))

@app.route('/marvel/movies/<int:movie_id>/delete', methods = ['POST'])
def deleteMovie(movie_id):
	if 'access_token' not in login_session or login_session['access_token'] is None:
		response = make_response(json.dumps('User not Logged in!'), 401)
		response.headers['Content-Type'] = "application/json"
		return response
	movie = session.query(Movie).filter_by(id = movie_id).one()
	if request.method == 'POST':
		session.delete(movie)
		session.commit()
		return redirect(url_for('showMovies'))

@app.route('/marvels/heroes/new', methods = ['GET', 'POST'])
def newHero():
	if 'access_token' not in login_session or login_session['access_token'] is None:
		response = make_response(json.dumps('User not Logged in!'), 401)
		response.headers['Content-Type'] = "application/json"
		return response
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
	app.secret_key = "super_secret_key"
	app.debug = True
	app.run(host='0.0.0.0', port=5000)