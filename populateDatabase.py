from flask import url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Character, Movie

engine = create_engine('sqlite:///marveldatabase.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

moviesList = session.query(Movie).all()

# Check if database already exists
if len(moviesList) != 0:
    for movie in moviesList:
        session.delete(movie)
    session.commit()

heroesList = session.query(Character).all()
if len(heroesList) != 0:
    for hero in heroesList:
        session.delete(hero)
    session.commit()


# Add the sample data.

thor = Movie(name="Thor",
             description="The epic adventure 'Thor'"
             "spans the Marvel Universe from present"
             "day Earth to the realm of Asgard. At"
             "the center of the story is The Mighty"
             "Thor, a powerful but arrogant warrior"
             "whose reckless actions reignite an"
             "ancient war. Thor is cast down to"
             "Earth and forced to live among humans"
             "as punishment. Once here, Thor learns"
             "what it takes to be a true hero when"
             "the most dangerous villain of his world"
             "sends the darkest forces of Asgard to"
             "invade Earth.",
             image_path="https://i.pinimg.com/564x/89"
             "/cf/02/89cf024822bb2f81734732d7dd07ee9e.jpg",
             created_by="nikhil97.nb@gmail.com")
session.add(thor)

doctorStrange = Movie(name="Doctor Strange",
                      description="From Marvel Studios comes"
                      "“Doctor Strange,” the story of world-famous"
                      "neurosurgeon Dr. Stephen Strange whose"
                      "life changes forever after a horrific car"
                      "accident robs him of the use of his hands."
                      "When traditional medicine fails him, he is"
                      "forced to look for healing, and hope, in"
                      "an unlikely place—a mysterious"
                      "enclave known as Kamar-Taj.",
                      image_path="http://is2.mzstatic.com/image"
                      "/thumb/Video122/v4/3b/48/9d/3b489da2-e266-4702"
                      "-85d6-a040dcdb944b/source/1200x630bb.jpg",
                      created_by="nikhil97.nb@gmail.com")
session.add(doctorStrange)

avengers = Movie(name="Avengers Age of Ultron",
                 description="Marvel's 'Avengers: Age"
                 "of Ultron' stars Robert Downey Jr., w"
                 "ho returns as Iron Man, along with"
                 "Chris Hemsworth as Thor, Mark Ruffalo"
                 "as Hulk and Chris Evans as Captain America.",
                 image_path="http://image.phimmoi.net"
                 "/film/1493/poster.medium.jpg",
                 created_by="tony@gmail.com")
session.add(avengers)

guardians = Movie(name="Guardians of the Galaxy",
                  description="Marvel's 'Guardians of"
                  "the Galaxy,' in theaters August 1,"
                  "expands the Marvel Cinematic Universe"
                  "into the cosmos, where brash adventurer Peter"
                  "Quill finds himself the object of an"
                  "unrelenting bounty hunt after stealing a"
                  "mysterious orb coveted by Ronan, a powerful"
                  "villain with ambitions that threaten the entire universe.",
                  image_path="https://images-na.ssl-images-"
                  "amazon.com/images/I/51T5sJngQLL.jpg",
                  created_by="starlord@gmail.com")
session.add(guardians)

thorCharacter = Character(name="Thor",
                          description="I am GOD of Thunder!!",
                          image_path="https://hottopic.scene7.com/is"
                          "/image/HotTopic/10449383_hi?$pdp_hero_standard$",
                          created_by="nikhil97.nb@gmail.com")
session.add(thorCharacter)

groot = Character(name="GROOT",
                  description="I am Groot!!",
                  image_path="https://vignette.wikia.nocookie.net"
                  "/disney/images/0/0b/GOTG2_-_Groot.png/revision"
                  "/latest/scale-to-width-down/515?cb=20170409114426",
                  created_by="nikhil97.nb@gmail.com")
session.add(groot)

tony = Character(name="Tony Stark",
                 description="You can't afford me!!",
                 image_path="https://dispatch.cdnserbe.net/"
                 "dispatch_image/2011/12/7/2011127125053mc2cyan_T5_15847.jpg",
                 created_by="tony@gmail.com")
session.add(tony)

natasha = Character(name="Natasha Romanoff",
                    description="Sun's gettin real low!",
                    image_path="https://i.pinimg.com/originals"
                    "/a2/8d/41/a28d41b45531eac158f8e9fbbc388778.jpg",
                    created_by="tony@gmail.com")
session.add(natasha)

session.commit()
