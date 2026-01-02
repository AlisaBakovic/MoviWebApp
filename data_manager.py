from http.client import responses

from flask import session, request
from models import db, User, Movie
from dotenv import load_dotenv
import os

load_dotenv()
OMDB_API_KEY = os.getenv('OMDB_API_KEY')


class DataManager:
    def get_users(self):
        return User.query.all()

    def add_user(self, name):

        new_user = User(name=name)

        db.session.add(new_user)
        db.session.commit()

    def fetch_movie_info(self, name):
        url = f"http://www.omdbapi.com/?t={name}&apikey={OMDB_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()


    def add_movie(self, user_id, name, year=None):

        new_movie = Movie(name=name, year=year, user_id=user_id)

        db.session.add(new_movie)
        db.session.commit()

    def update_movie_title(self, movie_id, new_name):

        movie = Movie.query.get(movie_id)

        if movie:
            movie.name = new_name
            db.session.commit()

    def delete_movie(self, movie_id):

        movie = Movie.query.get(movie_id)

        if movie:
            db.session.delete(movie)
            db.session.commit()

