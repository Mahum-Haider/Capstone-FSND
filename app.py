import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type, Authorization, true")

        response.headers.add("Access-Control-Allow-Methods",
                             "GET,PUT,POST,DELETE,OPTIONS")

        return response


    @app.route("/home")
    def handler():
        return jsonify({
            "success": True,
            'message': 'Working!'
        })


    # @app.route('/')
    # def get_greeting():
    #     excited = os.environ['EXCITED']
    #     greeting = "Hello" 
    #     if excited == 'true': 
    #         greeting = greeting + "!!!!! You are doing great in this Udacity project."
    #     return greeting

    # Movies
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        #Returns all movies
        movies = Movie.query.order_by(Movie.id).all()
        movies_list = []

        if len(movies) == 0:
            abort(404)
        else:
            for movie in movies:
                movies_list.append(movie.format())
        return jsonify({
            'success': True,
            'movies': movies_list
        })

    # Actors
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        #Returns all actors
        actors = Actor.query.order_by(Actor.id).all()
        actors_list = []

        if len(actors) == 0:
            abort(404)
        else:
            for actor in actors:
                actors_list.append(actor.format())
        return jsonify({
            'success': True,
            'actors': actors_list
        })

    return app

app = create_app()

if __name__ == '__main__':
    app.run(port=8080, debug=True)
