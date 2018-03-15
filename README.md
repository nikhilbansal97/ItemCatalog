## ItemCatalog

### This is a catalog of Marvel Movies and Characters

This project uses Flask Framework to create server and SQLAlchemy ORM to maintain the database of movies and characters.

### Requirements:

The project uses Python3 to run the server, so make sure it is installed.

Below are the modules needed to run the project:

* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Flask Framework](http://flask.pocoo.org/docs/0.12/)
* [OAuth2Client](https://github.com/google/oauth2client)
* [Requests](http://docs.python-requests.org/en/master/)
* [httplib2](https://github.com/httplib2/httplib2)

### Steps:
* Clone the Repository to your laptop.
* Run `database_setup.py` file to create a database that contains the tables for movies and characters.
* Run `populateDatabase.py` file to enter sample data to the database.
* Run `project_server.py` file to start the server. 
* Now you can access the catalog on `localhost:5000` address!

### JSON Endpoints

* To get the data from the database using the JSON Endpoints, **Login to the server.** 	

* The base url for every endpoint will be `localhost:5000`

* To access your `api-key`, click on the `API Token` button on the home page.

	#### 1. Get Movies:

	> /marvels/movies/json?api_key=your-api-key

	Example Response:
	
	```
	[
		{
			"description": "The epic adventure 'Thor' spans the Marvel Universe from present day Earth to the realm of Asgard. At the center of the story is The Mighty Thor, a powerful but arrogant warrior whose reckless actions reignite an ancient war. Thor is cast down to Earth and forced to live among humans as punishment. Once here, Thor learns what it takes to be a true hero when the most dangerous villain of his world sends the darkest forces of Asgard to invade Earth. ",
			"id": 1,
			"name": "Thor"
		},
		{
			"description": "From Marvel Studios comes “Doctor Strange,” the story of world-famous neurosurgeon Dr. Stephen Strange whose life changes forever after a horrific car accident robs him of the use of his hands. When traditional medicine fails him, he is forced to look for healing, and hope, in an unlikely place—a mysterious enclave known as Kamar-Taj.",
			"id": 2,
			"name": "Doctor Strange"
		},
		{
			"description": "Marvel's 'Avengers: Age of Ultron' stars Robert Downey Jr., who returns as Iron Man, along with Chris Hemsworth as Thor, Mark Ruffalo as Hulk and Chris Evans as Captain America.",
			"id": 3,
			"name": "Avengers Age of Ultron"
		},
		{
			"description": "Marvel's 'Guardians of the Galaxy,' in theaters August 1, expands the Marvel Cinematic Universe into the cosmos, where brash adventurer Peter Quill finds himself the object of an unrelenting bounty hunt after stealing a mysterious orb coveted by Ronan, a powerful villain with ambitions that threaten the entire universe.",
			"id": 4,
			"name": "Guardians of the Galaxy"
		}
	]
	```

	#### 2. Get Characters:

	> /marvels/characters/json?api-key=your-api-key

	Example Response:

	```
	[
		{
			"description": "I am GOD of Thunder!!",
			"id": 1,
			"name": "Thor"
		},
		{
			"description": "I am Groot!!",
			"id": 2,
			"name": "GROOT"
		},
		{
			"description": "You can't afford me!!",
			"id": 3,
			"name": "Tony Stark"
		},
		{
			"description": "Sun's gettin real low!",
			"id": 4,
			"name": "Natasha Romanoff"
		}
	]
	```
	
	#### 3. Get Movie details by id:

	> /marvels/movies/id-of-movie/json?api-key=your-api-key

	Example Response:

	```
	{
		"description": "From Marvel Studios comes “Doctor Strange,” the story of world-famous neurosurgeon Dr. Stephen Strange whose life changes forever after a horrific car accident robs him of the use of his hands. When traditional medicine fails him, he is forced to look for healing, and hope, in an unlikely place—a mysterious enclave known as Kamar-Taj.",
		"id": 2,
		"name": "Doctor Strange"
	}
	```

	#### 4. Get Character details by id:

	> marvels/characters/id-of-character/json?api-key=your-api-key

	Example Response:

	```
	{
		"description": "I am Groot!!",
		"id": 2,
		"name": "GROOT"
	}
	```



