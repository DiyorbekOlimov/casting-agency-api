import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import app
from models import setup_db, Actor, Movie
from flask_migrate import Migrate
from settings import *

assistant_header = {'Authorization': f'Bearer {ASSISTANT_TOKEN}'}
director_header = {'Authorization': f'Bearer {DIRECTOR_TOKEN}'}
producer_header = {'Authorization': f'Bearer {PRODUCER_TOKEN}'}


class CastingAgencyTestCase(unittest.TestCase):
    """This represents the casting-agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_path = DATABASE_URL
        self.db = setup_db(self.app, self.database_path)
        self.db.create_all()

        self.new_actor = {
            'age': 50,
            'gender': 'male',
            'name': 'John Doe'
        }

        self.update_actor = {
            'age': 90
        }

        self.new_movie = {
            'release_date': '2025-01-01',
            'title': 'New Movie'
        }

        self.update_movie = {
            'release_date': '2026-06-06'
        }

        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.app = self.app
        #     self.db.init_app(self.app)
        #     self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass


    # POST /actors

    def test_a_post_actors_401(self):
        res = self.client().post('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'unauthorized')

    def test_b_post_actors_400(self):
        res = self.client().post('/actors', headers=producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_c_post_actors(self):
        res = self.client().post('/actors', headers=producer_header, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)
        self.assertTrue(Actor.query.get(data['id']))


    # GET /actors

    def test_d_get_actors_401(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'unauthorized')

    def test_e_get_actors(self):
        res = self.client().get('/actors', headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actors'][0]['name'], self.new_actor['name'])
        self.assertEqual(data['actors'][0]['gender'], self.new_actor['gender'])
        self.assertEqual(data['actors'][0]['age'], self.new_actor['age'])
        self.assertEqual(data['all_actors'], 1)

    # GET /actors/<id>

    def test_f_get_actor_401(self):
        res = self.client().get('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'unauthorized')

    def test_g_get_actor(self):
        res = self.client().get('/actors/1', headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['age'], self.new_actor['age'])
        self.assertEqual(data['gender'], self.new_actor['gender'])
        self.assertEqual(data['name'], self.new_actor['name'])

    def test_h_get_actor_404(self):
        res = self.client().get('/actors/1000', headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'not found')


    # PATCH /actors

    def test_i_patch_actors_401(self):
        res = self.client().patch('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'unauthorized')

    def test_j_patch_actors_404(self):
        res = self.client().patch('/actors/1000', headers=director_header, json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'not found')

    def test_k_patch_actors(self):
        res = self.client().patch('/actors/1', headers=director_header, json=self.update_actor)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # DELETE /actors

    def test_l_delete_actors_401(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'unauthorized')

    def test_m_delete_actors_404(self):
        res = self.client().delete('/actors/1000', headers=producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'not found')

    def test_n_delete_actors(self):
        res = self.client().delete('/actors/1', headers=producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)



    # POST /movies

    def test_o_post_movies_401(self):
        res = self.client().post('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'unauthorized')

    def test_p_post_movies_400(self):
        res = self.client().post('/movies', headers=producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_q_post_movies(self):
        res = self.client().post('/movies', headers=producer_header, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)
        self.assertTrue(Movie.query.get(data['id']))


    # GET /movies

    def test_r_get_movies_401(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'unauthorized')

    def test_s_get_movies(self):
        res = self.client().get('/movies', headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movies'][0]['title'], self.new_movie['title'])
        self.assertEqual(data['movies'][0]['release_date'], self.new_movie['release_date'])
        self.assertEqual(data['all_movies'], 1)

    # GET /movies/<id>

    def test_t_get_movie_401(self):
        res = self.client().get('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'unauthorized')

    def test_u_get_movie(self):
        res = self.client().get('/movies/1', headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['title'], self.new_movie['title'])
        self.assertEqual(data['release_date'], self.new_movie['release_date'])

    def test_v_get_movie_404(self):
        res = self.client().get('/movies/1000', headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'not found')


    # PATCH /movies

    def test_w_patch_movies_401(self):
        res = self.client().patch('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'unauthorized')

    def test_x_patch_movies_404(self):
        res = self.client().patch('/movies/1000', headers=director_header, json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'not found')

    def test_y_patch_movies(self):
        res = self.client().patch('/movies/1', headers=director_header, json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # DELETE /movies

    def test_z1_delete_movies_401(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'unauthorized')

    def test_z2_delete_movies_404(self):
        res = self.client().delete('/movies/1000', headers=producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'not found')

    def test_z3_delete_movies(self):
        res = self.client().delete('/movies/1', headers=producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


if __name__ == '__main__':
    unittest.main()
