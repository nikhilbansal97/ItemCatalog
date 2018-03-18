from flask import Flask, render_template, url_for, request, jsonify, redirect
from flask import session as lSession
import random
import string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Character, Movie, User
# For signin
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

app = Flask(__name__)

engine = create_engine('sqlite:///marveldatabase.db')
Base.metadata.bind = engine

# Create a session object that is used to perform queries on the database.
Session = sessionmaker(bind=engine)
session = Session()

# The route for the home page of the catelog.


@app.route('/')
@app.route('/marvels/movies', methods=['GET', 'POST'])
def showMovies():
    mList = session.query(Movie).all()
    user = None
    # If the user is logged in then change the value of the variable.
    if 'access_token' not in lSession or lSession['access_token'] is None:
        login = 0
    else:
        login = 1
        user = session.query(User).filter_by(
            email=lSession['email']).one()
    info = (mList, "movies", login, user)
    return render_template('index.html', info=info)

# This function is used to get a random token so that it can be used as an
# api_key for the user.


def getRandomToken():
    api_token = ''.join(random.choice(
        string.ascii_lowercase + string.digits) for x in range(16))
    return api_token

# JSON endpoint to get a list of all the movies.


@app.route('/marvels/movies/json')
def getMoviesJson():
    # Get the query parameters as a dictionary.
    par = request.args
    # Checks to validate a well formed url.
    if 'access_token' not in lSession or lSession['access_token'] is None:
        response = make_response(json.dumps('User not Logged in!'), 401)
        response.headers['Content-Type'] = "application/json"
        return response
    if 'api_key' in par and len(par['api_key']) > 0:
        user = session.query(User).filter_by(
            api_key=par['api_key']).one_or_none()
        if user is None:
            response = make_response(json.dumps('Wrong API Key'), 401)
            response.headers['Content-Type'] = "application/json"
            return response
        else:
            mList = session.query(Movie).all()
            return jsonify([movie.serialize for movie in mList])
    elif 'api_key' not in par:
        response = make_response(json.dumps(
            'api_key parameter not found'), 401)
        response.headers['Content-Type'] = "application/json"
        return response
    elif len(par['api_key']) == 0:
        response = make_response(json.dumps('No api key found!'), 401)
        response.headers['Content-Type'] = "application/json"
        return response

# JSON Endpoint to get the characters in JSON format.


@app.route('/marvels/characters/json')
def getCharactersJson():
    par = request.args
    if 'access_token' not in lSession or lSession['access_token'] is None:
        response = make_response(json.dumps('User not Logged in!'), 401)
        response.headers['Content-Type'] = "application/json"
        return response
    if 'api_key' in par and len(par['api_key']) > 0:
        user = session.query(User).filter_by(
            api_key=par['api_key']).one_or_none()
        if user is None:
            response = make_response(json.dumps('Wrong API Key'), 401)
            response.headers['Content-Type'] = "application/json"
            return response
        else:
            characterList = session.query(Character).all()
            return jsonify([char.serialize for char in characterList])
    elif 'api_key' not in par:
        response = make_response(json.dumps(
            'api_key parameter not found'), 401)
        response.headers['Content-Type'] = "application/json"
        return response
    elif len(par['api_key']) == 0:
        response = make_response(json.dumps('No api key found!'), 401)
        response.headers['Content-Type'] = "application/json"
        return response

# Get the character information in JSON format according to the id.
# id: id of the character


@app.route('/marvels/characters/<int:id>/json')
def getSpecificCharacterJson(id):
    par = request.args
    if 'access_token' not in lSession or lSession['access_token'] is None:
        response = make_response(json.dumps('User not Logged in!'), 401)
        response.headers['Content-Type'] = "application/json"
        return response
    if 'api_key' in par and len(par['api_key']) > 0:
        user = session.query(User).filter_by(
            api_key=par['api_key']).one_or_none()
        if user is None:
            response = make_response(json.dumps('Wrong API Key'), 401)
            response.headers['Content-Type'] = "application/json"
            return response
        else:
            character = session.query(Character).filter_by(id=id).one_or_none()
            if character is None:
                response = make_response(json.dumps('No Character Found'), 401)
                response.headers['Content-Type'] = "application/json"
                return response
            return jsonify(character.serialize)
    elif 'api_key' not in par:
        response = make_response(json.dumps(
            'api_key parameter not found'), 401)
        response.headers['Content-Type'] = "application/json"
        return response
    elif len(par['api_key']) == 0:
        response = make_response(json.dumps('No api key found!'), 401)
        response.headers['Content-Type'] = "application/json"
        return response

# JSON Endpoint to get the information of the movie by id.
# id: id of the movie.


@app.route('/marvels/movies/<int:id>/json')
def getSpecificMoveiJson(id):
    par = request.args
    if 'access_token' not in lSession or lSession['access_token'] is None:
        response = make_response(json.dumps('User not Logged in!'), 401)
        response.headers['Content-Type'] = "application/json"
        return response
    if 'api_key' in par and len(par['api_key']) > 0:
        user = session.query(User).filter_by(
            api_key=par['api_key']).one_or_none()
        if user is None:
            response = make_response(json.dumps('Wrong API Key'), 401)
            response.headers['Content-Type'] = "application/json"
            return response
        else:
            movie = session.query(Movie).filter_by(id=id).one_or_none()
            if movie is None:
                response = make_response(json.dumps('No Movie Found'), 401)
                response.headers['Content-Type'] = "application/json"
                return response
            return jsonify(movie.serialize)
    elif 'api_key' not in par:
        response = make_response(json.dumps(
            'api_key parameter not found'), 401)
        response.headers['Content-Type'] = "application/json"
        return response
    elif len(par['api_key']) == 0:
        response = make_response(json.dumps('No api key found!'), 401)
        response.headers['Content-Type'] = "application/json"
        return response

# Login Endpoint that is used to get a random token for the session.


@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    # Save the random state generated in the lSession.
    lSession['state'] = state
    return render_template('login.html', STATE=state)

# Google Signin Endpoint that is being called when the user tries to sign in.


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Check if the connection is established and is secure
    if request.args.get('state') != lSession['state']:
        response = make_response(json.dumps('Invalid State Parameter'), 401)
        response.headers['Content-Type'] = "application/json"
        return response
    code = request.data
    try:
        # Upgrade the authorization code to credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope="")
        oauth_flow.redirect_uri = "postmessage"
        # Exchange the one time code with Google OAuth to get the credentials
        # object.
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code.', 401))
        response.headers['Content-Type'] = "application/json"
        return response
    # Check that the acess token is valid
    access_token = credentials.access_token
    url = ("https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s" %
           access_token)
    h = httplib2.Http()
    resp, content = h.request(url, 'GET')
    result = json.loads(content.decode('utf-8'))

    # If there was an error in access token, abort.
    if 'error' in result:
        response = make_request(json.dumps(
            "Token's user ID doesn't match the given user id"), 401)
        response.headers['Content-Type'] = "application/json"
        return response
    # Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
            "Token's user ID doesn't match the user id"), 401)
        response.headers['Content-Type'] = "application/json"
        return response
    if result['issued_to'] != ID:
        response = make_response(json.dumps(
            "Token's client ID doesn't match the app's"), 401)
        print("Token's client ID doesn't match the app's")
        response.headers['Content-Type'] = "application/json"
        return response
    # Check if user is already logged in.
    stored_credentials = lSession.get('access_token')
    stored_gplus_id = lSession.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps("User is already logged in"), 200)
        response.headers['Content-Type'] = "application/json"
        return response
    # Store the acess token in the login session for later use
    lSession['access_token'] = credentials.access_token
    lSession['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    lSession['username'] = data["name"]
    lSession['picture'] = data["picture"]
    lSession['email'] = data["email"]

    userInfo = session.query(User).filter_by(email=data["email"]).one_or_none()
    # If a new user is logged in, then generate an random api key and add it
    # to the Users table.
    if userInfo is None:
        newUser = User(name=data["name"], email=data[
                       "email"], api_key=getRandomToken())
        session.add(newUser)
        session.commit()

    output = ''
    output += '<h1>Welcome, '
    output += lSession['username']
    output += '!</h1>'
    output += '<img src="'
    output += lSession['picture']
    output += ' " style="width:300px;height:300px;'
    output += 'border-radius:150px;-webkit-border-radius:150px;'
    output += '-moz-border-radius:150px;"> '
    print("done!")
    return output

# The endpoint that is called when the user tries to logout.


@app.route('/gdisconnect')
def gdisconnect():
    # Check if the user is already logged out.
    if 'access_token' not in lSession or lSession['access_token'] is None:
        return redirect(url_for('showMovies'))
    access_token = lSession.get('access_token')
    if access_token is None:
        response = make_response('Currect user not connected.', 401)
        response.headers['Content-Type'] = "application/json"
        return response
    # Revoke the access token given by  Google OAuth.
    url = "https://accounts.google.com/o/oauth2/revoke?token=%s" % access_token
    h = httplib2.Http()
    resp, content = h.request(url, 'GET')
    print(content)
    print(resp.get('status'))
    print("Logged out!")
    lSession['state'] = None
    lSession['access_token'] = None
    return redirect(url_for('showMovies'))

# Endpoint to get the list of heroes.


@app.route('/marvels/heroes', methods=['GET', 'POST'])
def showHeroes():
    hList = session.query(Character).all()
    user = None
    if lSession['access_token'] is None:
        login = 0
    else:
        login = 1
        user = session.query(User).filter_by(
            email=lSession['email']).one()
    info = (hList, "heroes", login, user)
    return render_template('index.html', info=info)

# API Route to create the new Movie.


@app.route('/marvels/movies/new', methods=['GET', 'POST'])
def newMovie():
    # Check if the user is not signed in, then do nothing.
    if 'access_token' not in lSession or lSession['access_token'] is None:
        response = make_response(json.dumps('User not Logged in!'), 401)
        response.headers['Content-Type'] = "application/json"
        return response
    # If it is POST request, then create the new movie.
    if request.method == 'POST':
        name = request.form['inputName']
        description = request.form['inputDescription']
        link = request.form['inputLink']
        movie = Movie(name=name, description=description, image_path=link)
        session.add(movie)
        session.commit()
        return redirect(url_for('showMovies'))
    else:
        return render_template('newForm.html', new='movie')

# API Route to edit the movie.
# movie_id : id of the movie that is to be edited.


@app.route('/marvels/movies/<int:movie_id>/edit', methods=['GET', 'POST'])
def editMovie(movie_id):
    # If the user is not logged in, do nothing.
    if 'access_token' not in lSession or lSession['access_token'] is None:
        response = make_response(json.dumps('User not Logged in!'), 401)
        response.headers['Content-Type'] = "application/json"
        return response
    movie = session.query(Movie).filter_by(id=movie_id).one()
    # If it is a POST Request, then edit the movie
    if request.method == 'POST':
        name = request.form['inputName']
        if len(name) > 0:
            movie.name = name
        description = request.form['inputDescription']
        if len(description) > 0:
            movie.description = description
        image_path = request.form['inputLink']
        if len(image_path) > 0:
            movie.image_path = image_path
        session.add(movie)
        session.commit()
        return redirect(url_for('showMovies'))
    return render_template('editForm.html', movie=movie, edit="movie")

# API Endpoint to edit the hero
# hero_id : id of the hero that is to be edited.


@app.route('/marvel/heros/<int:hero_id>/edit', methods=['GET', 'POST'])
def editHero(hero_id):
    # If the user is lot logged in, do nothing.
    if 'access_token' not in lSession or lSession['access_token'] is None:
        response = make_response(json.dumps('User not Logged in!'), 401)
        response.headers['Content-Type'] = "application/json"
        return response
    hero = session.query(Character).filter_by(id=hero_id).one()
    # If it is POST request, only then edit the hero
    if request.method == 'POST':
        name = request.form['inputName']
        if len(name) > 0:
            hero.name = name
        description = request.form['inputDescription']
        if len(description) > 0:
            hero.description = description
        image_path = request.form['inputLink']
        if len(image_path) > 0:
            hero.image_path = image_path
        session.add(hero)
        session.commit()
        return redirect(url_for('showHeroes'))
    return render_template('editForm.html', hero=hero, edit="hero")

# API Endoint to delete the hero.
# hero_id : Id of the hero that is to be deleted.


@app.route('/marvel/heros/<int:hero_id>/delete', methods=['POST'])
def deleteHero(hero_id):
    # If the user is not logged in, do nothing.
    if 'access_token' not in lSession or lSession['access_token'] is None:
        response = make_response(json.dumps('User not Logged in!'), 401)
        response.headers['Content-Type'] = "application/json"
        return response
    hero = session.query(Character).filter_by(id=hero_id).one()
    # If it is POST request, only then delete the hero.
    if request.method == 'POST':
        session.delete(hero)
        session.commit()
        return redirect(url_for('showHeroes'))

# API Endpoint to delete the movie.
# movie_id : Id of the movie that is to be deleted.


@app.route('/marvel/movies/<int:movie_id>/delete', methods=['POST'])
def deleteMovie(movie_id):
    # If the user is not logged in, then no nothing.
    if 'access_token' not in lSession or lSession['access_token'] is None:
        response = make_response(json.dumps('User not Logged in!'), 401)
        response.headers['Content-Type'] = "application/json"
        return response
    movie = session.query(Movie).filter_by(id=movie_id).one()
    # If it is a POST request, only then delete the movie.
    if request.method == 'POST':
        session.delete(movie)
        session.commit()
        return redirect(url_for('showMovies'))

# API Endpoint to create a new hero.


@app.route('/marvels/heroes/new', methods=['GET', 'POST'])
def newHero():
    # If the user is not logged in, do nothing.
    if 'access_token' not in lSession or lSession['access_token'] is None:
        response = make_response(json.dumps('User not Logged in!'), 401)
        response.headers['Content-Type'] = "application/json"
        return response
    # If it is POST Request, only then create a new hero.
    if request.method == 'POST':
        name = request.form['inputName']
        description = request.form['inputDescription']
        link = request.form['inputLink']
        hero = Character(name=name, description=description, image_path=link)
        session.add(hero)
        session.commit()
        return redirect(url_for('showHeroes'))
    else:
        return render_template('newForm.html', new='hero')


if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
