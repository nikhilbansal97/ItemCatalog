from flask import url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Character, Movie

engine = create_engine('sqlite:///marveldatabase.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

ironMan = Movie(id = 1, name = "Iron Man(2008)", description = "2008's Iron Man tells the story of Tony Stark, a billionaire industrialist and genius inventor who is kidnapped and forced to build a devastating weapon. Instead, using his intelligence and ingenuity, Tony builds a high-tech suit of armor and escapes captivity. When he uncovers a nefarious plot with global implications, he dons his powerful armor and vows to protect the world as Iron Man.", image_path = "https://cdn.shopify.com/s/files/1/1402/3931/products/ironman_1024x1024.png?v=1509419814")

session.add(ironMan)

hulk = Movie(id = 2, name = "The Incredible Hulk", description = "'The Incredible Hulk' kicks off an all-new, explosive and action-packed epic of one of the most popular super heroes of all time. In this new beginning, scientist Bruce Banner (Edward Norton) desperately hunts for a cure to the gamma radiation that poisoned his cells and unleashes the unbridled force of rage within him: The Hulk. Living in the shadows--cut off from a life he knew and the woman he loves, Betty Ross (Liv Tyler)--Banner struggles to avoid the obsessive pursuit of his nemesis, General Thunderbolt Ross (William Hurt) and the military machinery that seeks to capture him and brutally exploit his power. ", image_path = "https://images-na.ssl-images-amazon.com/images/M/MV5BMTUyNzk3MjA1OF5BMl5BanBnXkFtZTcwMTE1Njg2MQ@@._V1_QL50_SY1000_CR0,0,674,1000_AL_.jpg")

session.add(hulk)

thor = Movie(id = 3, name = "Thor", description = "The epic adventure 'Thor' spans the Marvel Universe from present day Earth to the realm of Asgard. At the center of the story is The Mighty Thor, a powerful but arrogant warrior whose reckless actions reignite an ancient war. Thor is cast down to Earth and forced to live among humans as punishment. Once here, Thor learns what it takes to be a true hero when the most dangerous villain of his world sends the darkest forces of Asgard to invade Earth. ", image_path = "https://i.pinimg.com/564x/89/cf/02/89cf024822bb2f81734732d7dd07ee9e.jpg")

session.add(thor)

session.commit()