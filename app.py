from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth import requires_auth, AuthError
from errors import errors


app = Flask(__name__)
db = setup_db(app)
db.create_all()
CORS(app)

COUNT_PER_PAGE = 5

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response


@app.route('/')
def index():
    return 'server is working'


@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors():
    page = request.args.get('page', 1, type=int)
    actors = [actor.format() for actor in Actor.query.all()]
    start = COUNT_PER_PAGE * (page - 1)
    end = start + COUNT_PER_PAGE
    selection = actors[start:end]
    if len(selection) == 0: abort(404)
    return jsonify({
        'success': True,
        'actors': selection,
        'all_actors': len(actors)
    })


@app.route('/actors/<int:id>', methods=['GET'])
@requires_auth('get:actors')
def get_actor(id):
    actor = Actor.query.get(id)
    if actor is None: abort(404)
    return jsonify({
        'success': True,
        'id': actor.id,
        'name': actor.name,
        'age': actor.age,
        'gender': actor.gender
    })


@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def post_actors():
    req = request.get_json()
    if req is None: abort(400)
    name = req.get('name', None)
    age = req.get('age', None)
    gender = req.get('gender', None)
    if name is None or age is None or gender is None: abort(400)
    actor = Actor(name, age, gender)
    if actor is None: abort(400)
    actor.add()
    return jsonify({
        'success': True,
        'id': actor.id
    })


@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actors')
def patch_actors(id):
    req = request.get_json()
    if req is None: abort(400)
    actor = Actor.query.get(id)
    if actor is None: abort(404)
    actor.name = req.get('name', actor.name)
    actor.age = req.get('age', actor.age)
    actor.gender = req.get('gender', actor.gender)
    actor.update()
    return jsonify({
        'success': True
    })


@app.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actors(id):
    actor = Actor.query.get(id)
    if actor is None: abort(404)
    actor.delete()
    return jsonify({
        'success': True
    })



@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies():
    page = request.args.get('page', 1, type=int)
    movies = [movie.format() for movie in Movie.query.all()]
    start = COUNT_PER_PAGE * (page - 1)
    end = start + COUNT_PER_PAGE
    selection = movies[start:end]
    if len(selection) == 0: abort(404)
    return jsonify({
        'success': True,
        'movies': movies,
        'all_movies': len(movies)
    })


@app.route('/movies/<int:id>', methods=['GET'])
@requires_auth('get:movies')
def get_movie(id):
    movie = Movie.query.get(id)
    if movie is None: abort(404)
    return jsonify({
        'success': True,
        'id': movie.id,
        'title': movie.title,
        'release_date': movie.release_date
    })


@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def post_movies():
    req = request.get_json()
    if req is None: abort(400)
    title = req.get('title', None)
    rdate = req.get('release_date', None)
    if title is None or rdate is None: abort(400)
    movie = Movie(title, rdate)
    movie.add()
    return jsonify({
        'success': True,
        'id': movie.id
    })


@app.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movies')
def patch_movies(id):
    movie = Movie.query.get(id)
    if movie is None: abort(404)
    req = request.get_json()
    if req is None: abort(400)
    title = req.get('title', movie.title)
    rdate = req.get('release_date', movie.release_date)
    movie.title = title
    movie.release_date = rdate
    movie.update()
    return jsonify({
        'success': True
    })


@app.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movies(id):
    movie = Movie.query.get(id)
    if movie is None: abort(404)
    movie.delete()
    return jsonify({
        'success': True
    })


@app.errorhandler(400)
def bad_request(e):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400

@app.errorhandler(401)
def unauthorized(e):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'unauthorized'
    }), 401

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'not found'
    }), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
    })

@app.errorhandler(AuthError)
def auth_error(ex):
    return jsonify({
        'success': False,
        'error': ex.status_code,
        'message': errors[ex.status_code],
        'description': ex.description
    }), ex.status_code


if __name__ == '__main__':
    app.run()
