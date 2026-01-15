import os
from models import db
from models import setup_db, Actor, Movie
from flask_migrate import Migrate
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from auth import requires_auth, AuthError


def create_app(test_config=None):

    app = Flask(__name__)
    #setup_db(app)
    migrate = Migrate(app, db) 
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED', 'false']
        greeting = "Hello" 
        if excited == 'true': 
            greeting = greeting + "!!!!! You are doing great in this Udacity project."
        return greeting

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        return jsonify({"success": True, "actors": [a.format() for a in actors]})

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()
        if not body:
            abort(400)
        
        actor = Actor(
            name=body.get('name'),
            age=body.get('age'),
            gender=body.get('gender'))
        
        actor.insert()
        return jsonify({"success": True, "actor": actor.format()})

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)
        body = request.get_json()
        if 'name' in body:
            actor.name = body['name']
        actor.update()
        return jsonify({"success": True, "actor": actor.format()})

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)
        actor.delete()
        return jsonify({"success": True,"delete": actor_id})
    

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()
        return jsonify({"success": True,"movies": [m.format() for m in movies]})

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()
        if not body:
            abort(400)
        
        title = body.get('title')
        release_date = body.get('release_date')
        
        if not title:
            abort(400)
            
        movie = Movie(title=title,release_date=release_date)
        movie.insert()
        
        return jsonify({"success": True,"movie": movie.format()})

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)
            
        body = request.get_json()
        if not body:
            abort(400)
        
        if 'title' in body:
            movie.title = body['title']
        if 'release_date' in body:
            movie.release_date = body['release_date']
            
        movie.update()
        return jsonify({
            "success": True,
            "movie": movie.format()
            })


    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)
            
        movie.delete()
        
        return jsonify({"success": True,"delete": movie_id})


    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"
    

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400}), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404}), 404
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False, "error": 422}), 422
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"success": False, "error": 500}), 500
    
    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        return jsonify({"success": False, "error": ex.status_code, "message": ex.error}), ex.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
