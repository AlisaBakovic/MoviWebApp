from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from data_manager import DataManager
from models import db, Movie, User


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movieweb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
data_manager = DataManager()

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    users = data_manager.get_users()
    return render_template('users.html', users=users)

@app.route('/users')
def list_users():
    users = data_manager.get_users()
    return render_template('users.html', users=users)

@app.route('/users', methods=['POST'])
def create_users():
    name = request.form.get('name')
    data_manager.add_user(name)
    return redirect('/')

@app.route('/users/<int:user_id>/movies', methods=['GET'])
def user_movies(user_id):

    user = User.query.get(user_id)
    movies = Movie.query.filter_by(user_id=user_id).all()
    return render_template('movies.html', user=user, movies=movies)

@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):

    name = request.form.get('name')
    year = request.form.get('year')
    year = int(year) if year else None

    data_manager.add_movie(user_id, name, year)

    return redirect(f'/users/{user_id}/movies')

@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):

    new_name = request.form.get('name')

    data_manager.update_movie_title(movie_id, new_name)

    return redirect(f'/users/{user_id}/movies')

@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):

    data_manager.delete_movie(movie_id)
    return redirect(f'/users/{user_id}/movies')

if __name__ == '__main__':
    app.run(debug=True, port=5001)