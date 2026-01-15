import os
import unittest
import json

from app import create_app
from models import setup_db, Actor, Movie, db


casting_assistant_token = os.environ.get('CASTING_ASSISTANT_TOKEN')
casting_director_token = os.environ.get('CASTING_DIRECTOR_TOKEN')
executive_producer_token = os.environ.get('EXECUTIVE_PRODUCER_TOKEN')

database_path = 'sqlite:///:memory:'

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        
        self.app = create_app()
        self.client = self.app.test_client

        self.database_path = database_path

        with self.app.app_context():
            db.create_all()
        self.assertIsNotNone(casting_assistant_token)
        self.assertIsNotNone(casting_director_token)
        self.assertIsNotNone(executive_producer_token)

        self.new_actor = {
            "name": "Test Actor",
            "age": 30,
            "gender": "Male"
        }

        self.new_movie = {
            "title": "Test Movie",
            "release_date": "2025"
        }

        self.headers_assistant = {
            "Authorization": f"Bearer {casting_assistant_token}"
        }

        self.headers_director = {
            "Authorization": f"Bearer {casting_director_token}"
        }

        self.headers_producer = {
            "Authorization": f"Bearer {executive_producer_token}"
        }
    def test_get_actors_success(self):
            res = self.client().get('/actors', headers=self.headers_assistant)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            
    def test_create_actor_success(self):
            res = self.client().post('/actors',headers=self.headers_director,json=self.new_actor)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            
    def test_delete_movie_success(self):
        with self.app.app_context():    
            movie = Movie(title="Temp", release_date="2024")
            movie.insert()
            res = self.client().delete(f'/movies/{movie.id}',headers=self.headers_producer)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            
    def test_assistant_cannot_create_actor(self):
            res = self.client().post('/actors',headers=self.headers_assistant,json=self.new_actor)
            self.assertEqual(res.status_code, 403)
            
    def test_director_cannot_delete_movie(self):
        with self.app.app_context():
            movie = Movie(title="Protected", release_date="2024")
            movie.insert()
            res = self.client().delete(f'/movies/{movie.id}',headers=self.headers_director)
            self.assertEqual(res.status_code, 403)
        
    def test_missing_token(self):
            res = self.client().get('/actors')
            self.assertEqual(res.status_code, 401)
        
    def test_delete_actor_not_found(self):
            res = self.client().delete('/actors/99999',headers=self.headers_producer)
            self.assertEqual(res.status_code, 404)

    def tearDown(self):
        with self.app.app_context():
              db.session.remove()
              db.drop_all()

if __name__ == '__main__':
    unittest.main()

