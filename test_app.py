import os
import sys
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor, db_create_all
from app import create_app

sys.path.insert(0, '..')

class CastingAgencyTestCase(unittest.TestCase):
    #This class represents the Casting Agency test case

    def setUp(self):
        #Define test variables and initialize app.
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castingagency_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)

       
        setup_db(self.app, self.database_path)

        self.ASSISTANT_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxfLXJvdGtFNktRS3Jla3NVaVllMyJ9.eyJpc3MiOiJodHRwczovL2Rldi0yYW84cTVuby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjI1NWQ4Zjg5MDQ4ODYwMDY5MDBlYzdlIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTY1MDczODE0NywiZXhwIjoxNjUwNzQ1MzQ3LCJhenAiOiJDZVNrSnJWMm42OG9lSEs0ZzE1MkNMQkliTFd4TWRvZyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.MYCZ_Xlx7dPk_yI7KLiSKZtILtwoXl88Zl0MI2f84i6_r0bAty34rTnjFJJHkI7LksJGLPptHuC15QLUwDNeJ78m4JYc-9Glmz5eitJv5UQeSQEARFl2M2KBbjQUWV51pfEN7RitxzmaeilwjuVw63NZvoebykNDrI09b-GZW0M9hp3o9aYRFN_1ahjAerKa1W1Gb0mAOrsd6zBj2iAZtEJXaxHp5lDsH0NFjdE4Q1hedpvULcCIrU2a4z0N99qMotAEqVJ2zf3j_YWeInvdswcesRVgCJSUCqDutFqbB1mg4RSlh-olSfjnbaUREJ5UwaoiyPMfYCmofRxdIm4ghw&expires_in=7200"
        self.DIRECTOR_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxfLXJvdGtFNktRS3Jla3NVaVllMyJ9.eyJpc3MiOiJodHRwczovL2Rldi0yYW84cTVuby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjI1NWQ4YmFkNzc4MmIwMDZmMzEwMjY5IiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTY1MDczODA5MywiZXhwIjoxNjUwNzQ1MjkzLCJhenAiOiJDZVNrSnJWMm42OG9lSEs0ZzE1MkNMQkliTFd4TWRvZyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.qvHN_qj8qIrIZbodfGGT2vwM6z0H9rJbH6greo7U5euXty-ZqFxAKLM5odiBBm0R-nBzF4pj7ZqB3sl9zJ_ppSqbTTmTIBhBiYPYcjVcl-anGEEvpTr609ZVRK6hYu46UGmhxvUxmc5EHdCyI4ZdQWPiYGTbykMEcHjmidhZNjDyAa2_Y9Rpu2zFaRgptHrZgofSdyUPQ3GwUYD57XTYoPj8k3nDsK23xcW243R4T6ZKAp36M7So0zIQBa_d3c-nY4txrbMMInWA4vAmNmptL7DPXhwQFyizrwv8rX3fyTAgrHV2IXu0hxerKJVfhqvu2lYzQfhSnajNA15FWl7LtQ"
        self.PRODDUCER_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxfLXJvdGtFNktRS3Jla3NVaVllMyJ9.eyJpc3MiOiJodHRwczovL2Rldi0yYW84cTVuby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE1Nzc4MjdjYWMzN2YwMDY4NDQzY2Q1IiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTY1MDczODAzNCwiZXhwIjoxNjUwNzQ1MjM0LCJhenAiOiJDZVNrSnJWMm42OG9lSEs0ZzE1MkNMQkliTFd4TWRvZyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.adR97mEf9K-Ir1Dve0xGYoB9G3U0SqnBYfD_ZKbIOguDcIM6yEcaXfnT_FbC1eON9LltPdeM_XEnuLNgmTeuoQ0nqQo0HReqnaHLjWNoUM3BeVaOsylOWSeGYdooTtevoKHXJWDs1JGSmOQ9sguwptCqbDxs3MNAQ746nhSeQu-Z3oFC6390Vwug_K-AbIsSL69zYhunuz47OfUhvVBwezqOfq7WaVJIQA9ZJhfMevXzfVoaQ0cMujlg2bTbBzpHTFLTGiYP4Bew5JRta1U_OfRcR2ZsX8YVs1i7GhAVljhr_N1lGtz94IZfwSch2uoFtlAboa0vjmlWL6HHy7Ckmg"


    
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        #Executed after each test
        pass

    # General Test - Server status
    def test_server_status(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

# # GET Endpoints: 

    #GET Actors
    def test_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization': 'Bearer {}'.format(self.ASSISTANT_TOKEN)})
                             
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        #self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']))
        self.assertTrue(data['total_actors'])

    #GET Actors Fail
    def test_401_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    #GET Movies
    def test_get_movies(self):
        res = self.client().get('movies',
                                headers={'Authorization': 'Bearer {}'.format(self.ASSISTANT_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    #GET Movies Fail
    def test_401_get_movies(self):
        res = self.client().get('/movies',
                                headers={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    #POST Actors
    def test_create_actor(self):
        res = self.client().post('/actors',
                                 headers={'Authorization': 'Bearer {}'.format(self.PRODDUCER_TOKEN)}, json={'name': 'John'})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created actor'])

    #POST Actors Fail
    def test_401_create_actor(self):
        res = self.client().post('/actors',
                                 headers={'Authorization': 'Bearer {}'.format(self.PRODDUCER_TOKEN)}, json={'age': 20})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

     #POST Movies
     def test_create_movie(self):
        res = self.client().post('/movies',
                                 headers={'Authorization': 'Bearer {}'.format(self.PRODDUCER_TOKEN)}, json={'title': 'Testing01'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created movie'])

    #POST Movies Fail
    def test_401_create_movie(self):
        res = self.client().post('/movies',
                                 headers={'Authorization': 'Bearer {}'.format(self.PRODDUCER_TOKEN)}, json={'release_date': '1991'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    #PATCH Actors
    def test_update_actor(self):
        res = self.client().patch('/actors/1',
                                  headers={'Authorization': 'Bearer {}'.format(self.PRODDUCER_TOKEN)}, json={'name': 'John Test'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    #PATCH Actors Fail
    def test_401_update_actor(self):
        res = self.client().patch('/actors/1',
                                  headers={'Authorization': 'Bearer {}'.format(self.PRODDUCER_TOKEN)}, json={'name': 'John'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    #PATCH Movies
    def test_update_movie(self):
        res = self.client().patch('/movies/1',
                                  headers={'Authorization': 'Bearer {}'.format(self.PRODDUCER_TOKEN)}, json={'title': 'update test'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    #PATCH Movies Fail
    def test_401_update_movie(self):
        res = self.client().patch('/movies/1',
                                  headers={'Authorization': 'Bearer {}'.format(self.PRODDUCER_TOKEN)}, json={'release_date': '2001'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    #DELETE Actors
    def test_delete_actor(self):
        res = self.client().delete('/actors/1',
                                   headers={'Authorization': 'Bearer {}'.format(self.PRODDUCER_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    #DELETE Actors Fail
    def test_401_delete_actor(self):
        res = self.client().delete('/actors/1',
                                   headers={'Authorization': 'Bearer {}'.format(self.ASSISTANT_TOKEN)})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    #DELETE Movies
    def test_delete_movie(self):
        res = self.client().delete('movies/1',
                                   headers={'Authorization': 'Bearer {}'.format(self.ASSISTANT_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    #DELETE Movies Fail
    def test_401_delete_movie(self):
        res = self.client().delete('movies/1',
                                   headers={'Authorization': 'Bearer {}'.format(self.ASSISTANT_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()