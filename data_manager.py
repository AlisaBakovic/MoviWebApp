from models import db, User, Movie
from dotenv import load_dotenv
import os
import requests

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
            if data.get("Response") == "True":
                return {
                    "name": data.get("Title"),
                    "director": data.get("Director"),
                    "year": int(data.get("Year")) if data.get("Year") else None,
                    "poster_url": data.get("Poster")
                }
            return None



    def add_movie(self, user_id, movie_name):

        info = self.fetch_movie_info(movie_name)

        if info:
            new_movie = Movie(
                name=info['name'],
                director=info['director'],
                year=info['year'],
                poster_url=info['poster_url'],
                user_id=user_id
            )

            db.session.add(new_movie)
            db.session.commit()
            return new_movie
        return None

    def update_movie_title(self, movie_id, new_name):

        movie = Movie.query.get(movie_id)

        if movie:
            movie.name = new_name
            db.session.commit()

    def delete_movie(self, movie_id):

        movie = Movie.query.get(movie_id)

        if not movie:
            return False

        db.session.delete(movie)
        db.session.commit()

