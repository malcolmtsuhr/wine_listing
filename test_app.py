import os
import unittest
import json
import re
from flask_sqlalchemy import SQLAlchemy
from flask import (
    Flask, render_template, request, abort, session,
    Response, flash, jsonify, redirect, url_for)
from app import create_app
from models import (
	setup_db, Vintner, Vino)


class VinoTestCase(unittest.TestCase):
	"""This class represents the wine cellar test case"""

	def setUp(self):
		"""Define test variables and initialize app."""
		self.app = create_app()
		self.client = self.app.test_client
		self.database_name = "vino_test"
		self.database_path = 'postgresql://malcolmsuhr@localhost:5432/vino_test'
		setup_db(self.app, self.database_path)
		self.app.config['TESTING'] = True
		self.app.config['WTF_CSRF_ENABLED'] = False

		# binds the app to the current context
		with self.app.app_context():
			self.db = SQLAlchemy()
			self.db.init_app(self.app)
			# create all tables
			self.db.create_all()

		self.test_vintner = {
			'name': 'Ridge Vineyards',
			'country': 'United States',
			'region': 'california',
			'appellation': 'sonoma county',
			'website': '',
			'image_link': 'https://images.unsplash.com/photo-1560493676-04071c5f467b?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=968&q=80',
			'creation_date': '2021-02-28 19:24:37'
		}

		self.test_vino = {
			'name': 'Lytton Springs',
			'year': '2018',
			'type': '3',
			'varietal': '{Zinfandel,"Pinot Noir"}',
			'style': 'Bold',
			'abv': '11.11',
			'image_link': 'https://images.unsplash.com/photo-1586370434639-0fe43b2d32e6?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=634&q=80',
			'creation_date': '2021-02-28 21:15:54',
			'vintner_id': '2',
		}

		self.cellar_admin = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlRFeDZyZW9jaWhTbDFRNnBRVndoZSJ9.eyJpc3MiOiJodHRwczovL210c3VocjIwMjEudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwNDZiMTEwM2ZlMzI1MDA2OWY1OGE2YSIsImF1ZCI6WyJodHRwOi8vMC4wLjAuMTo4MDgwIiwiaHR0cHM6Ly9tdHN1aHIyMDIxLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MTYwMjkyMzUsImV4cCI6MTYxNjExNTYzNSwiYXpwIjoibjFySlZDdHZrWFpVallpRnlwTEdwMjA2cG84TUZtc1MiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnZpbnRuZXJzIiwiZGVsZXRlOndpbmVzIiwiZ2V0OmF1dGgiLCJnZXQ6dmludG5lcnMtY3JlYXRlIiwiZ2V0OnZpbnRuZXJzLWVkaXQiLCJnZXQ6d2luZXMtY3JlYXRlIiwiZ2V0OndpbmVzLWVkaXQiLCJwb3N0OnZpbnRuZXJzLWNyZWF0ZSIsInBvc3Q6dmludG5lcnMtZWRpdCIsInBvc3Q6d2luZXMtY3JlYXRlIiwicG9zdDp3aW5lcy1lZGl0Il19.ISe2PRWgWyz83kHFbQ1HnUQt6eeeN3jQavJOKjOz3SZ1xXWvWhRe8HIZMQO3WAwS3Z86CPEEgk-v2Jyf8bGf4M6iZ2zZMVPE017jH5_vCyJrQF6Ght3mSl7RmJuI7FSfe4zSMFfj5R1svhfryAB0rCpUhhW_rpRcW9g5uy7mXGck3G2ssPaybEkNHnS7OSW5vypKv9TfxJn5Rb9F_V1_O2sFgnv4hDkLDcng_clV4jPjYYmekGluloszl6uMeFR2FGYwE5E4D9NtOONNwzg8kEr8hXpFvf_Ur1rmq0S-2S9DpPpKOsEeTAd2i-dP47FdxfMQ2DpJ1ITugv9pjR4z7g'

		self.cellar_manager = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlRFeDZyZW9jaWhTbDFRNnBRVndoZSJ9.eyJpc3MiOiJodHRwczovL210c3VocjIwMjEudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwNGJlNTQwYWRkNWM4MDA2ZmUzNzM1NSIsImF1ZCI6WyJodHRwOi8vMC4wLjAuMTo4MDgwIiwiaHR0cHM6Ly9tdHN1aHIyMDIxLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MTYwMjkyNzIsImV4cCI6MTYxNjExNTY3MiwiYXpwIjoibjFySlZDdHZrWFpVallpRnlwTEdwMjA2cG84TUZtc1MiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZ2V0OmF1dGgiLCJnZXQ6dmludG5lcnMtY3JlYXRlIiwiZ2V0OnZpbnRuZXJzLWVkaXQiLCJnZXQ6d2luZXMtY3JlYXRlIiwiZ2V0OndpbmVzLWVkaXQiLCJwb3N0OnZpbnRuZXJzLWNyZWF0ZSIsInBvc3Q6dmludG5lcnMtZWRpdCIsInBvc3Q6d2luZXMtY3JlYXRlIiwicG9zdDp3aW5lcy1lZGl0Il19.me8n__h1liwCHVLbR6J_bbyKzCtOhQGhFmNA8tun8ldsZ1KNhK-GkL6sCC4zgsV80_JbWlC4ZdL0mTZsImF8HkHFZjSgj8asmat1MCNvkatVmhrZPn6PSVSaYH9bYsRCjJiQ9Iq94SY6cChWh6oQNF1pqw8IR6xz9fgZrzLWAiIq7ptYU5V2gbImnwOdDZbobsPAJ5vgNNGGRB8ZcIqe4WPN26d0T8N8AFudYrU0ema-1GNxcUFwI9n4yzKv32Aoc9lPG0c5y_aSi0XUmlYOR3hwjXNArd8wo_6dZdUhDO0_3DuRuN-u28FkhrLFadUUrLmnwYdMiM90ZPElh5Pmpw'


	def tearDown(self):
		"""Executed after each test"""
		pass

	"""
	TESTS
	Includes at least one test for expected success
	and error behavior for each endpoint

	Includes tests demonstrating role-based access control,
	at least two per role.
	"""

	"""
	Tests for vintners endpoints
	includes RBAC
	"""

# Get vintners list test set
	def test_get_vintners(self):
		res = self.client().get('/vintners', follow_redirects=True)
		data = (res.data)
		self.assertEqual(res.status_code, 200)
		self.assertTrue(data)

	def test_get_vintners_error(self):
		res = self.client().get('/vintner')
		data = (res.data)
		self.assertEqual(res.status_code, 404)

# Get vintner details test set
	def test_get_vintner_details(self):
		res = self.client().get('/vintners/2', follow_redirects=True)
		data = (res.data)
		self.assertEqual(res.status_code, 200)
		self.assertTrue(data)

	def test_get_vintner_details_does_not_exist(self):
		res = self.client().get('/vintner/1000', follow_redirects=True)
		data = (res.data)
		self.assertEqual(res.status_code, 404)

# Post create vintner form test set
	def test_post_new_vintner(self):
		res = self.client().post('/vintners/create', data=self.test_vintner, headers={'Authorization': 'bearer ' + self.cellar_admin}, follow_redirects=True)
		data = (res.data)
		self.assertEqual(res.status_code, 200)
		self.assertTrue(re.search('successfully listed!',
                    res.get_data(as_text=True)))

# RBAC - no auth test for post : create vintner
	def test_401_no_rbac_vintner_create(self):
		res = self.client().post('/vintners/create', data=self.test_vintner, headers={"Authorization": f'bearer none'})
		data = (res.data)
		self.assertEqual(res.status_code, 401)

# Get edit vintner form test set
# RBAC - with edit permissions
	def test_get_edit_vintner_by_manager(self):
		res = self.client().get('/vintners/2/edit', headers={"Authorization": f'bearer {self.cellar_admin}'})
		data = res.data
		self.assertEqual(res.status_code, 200)

# RBAC - no auth edit permissions
	def test_get_edit_vintner_no_auth(self):
		res = self.client().get('/vintners/2/edit', headers={"Authorization": f'bearer none'})
		data = res.data
		self.assertEqual(res.status_code, 401)

# Post edit vintner form test set
	def test_update_vintner(self):
		res = self.client().post('/vintners/2/edit', data=self.test_vintner, headers={'Authorization': 'bearer ' + self.cellar_admin}, follow_redirects=True)
		data = (res.data)
		self.assertEqual(res.status_code, 200)
		self.assertTrue(re.search('successfully edited!', res.get_data(as_text=True)))

	def test_update_vintner_badurl(self):
		res = self.client().post('/vintners/1000/edit', data=self.test_vintner, headers={'Authorization': 'bearer ' + self.cellar_admin})
		data = (res.data)
		self.assertEqual(res.status_code, 302)
		self.assertFalse(re.search('An error occurred.',
                    res.get_data(as_text=True)))

# Delete vintner test sets
# RBAC - no permission auth test for delete : vintner by Manager Role
	def test_delete_vintner_no_rbac(self):
		id = 1
		res = self.client().delete(f'/vintners/{id}', headers={"Authorization": f'bearer {self.cellar_manager}'}, follow_redirects=True)
		self.assertEqual(res.status_code, 401)

# RBAC - with permission auth test for delete : vintner by Admin Role
	def test_delete_vintner(self):
		vintner_delete = Vintner.query.filter(Vintner.name == "Ridge Vineyards").one_or_none()
		id = vintner_delete.id
		res = self.client().delete(f'/vintners/{id}', headers={"Authorization": f'bearer {self.cellar_admin}'}, follow_redirects=True)
		data = (res.data)
		vintner = Vintner.query.filter(Vintner.id == id).one_or_none()
		self.assertEqual(res.status_code, 200)
		self.assertEqual(vintner, None)

	def test_delete_vintner_does_not_exist(self):
		res = self.client().delete('/vintners/1000', headers={"Authorization": f'bearer {self.cellar_admin}'})
		# redirect for out of range url call
		self.assertEqual(res.status_code, 302)

	"""
	Tests for vino endpoints
	includes RBAC
	"""

# Get wines list test set
	def test_get_wines(self):
		res = self.client().get('/wines', follow_redirects=True)
		data = (res.data)
		self.assertEqual(res.status_code, 200)
		self.assertTrue(data)

	def test_get_wines_error(self):
		res = self.client().get('/wine')
		data = (res.data)
		self.assertEqual(res.status_code, 404)

# Get wine details test set
	def test_get_wine_details(self):
		res = self.client().get('/wines/2', follow_redirects=True)
		data = (res.data)
		self.assertEqual(res.status_code, 200)
		self.assertTrue(data)

	def test_get_wine_details_does_not_exist(self):
		res = self.client().get('/wine/1000', follow_redirects=True)
		data = (res.data)
		self.assertEqual(res.status_code, 404)

# Post create wine form test set
	def test_post_new_wine(self):
		res = self.client().post('/vintners/2/vino/create', data=self.test_vino, headers={'Authorization': 'bearer ' + self.cellar_admin}, follow_redirects=True)
		data = (res.data)
		self.assertEqual(res.status_code, 200)
		self.assertTrue(re.search('successfully listed!',
                    res.get_data(as_text=True)))

# RBAC - no auth test for post : create wine
	def test_401_no_rbac_wine_create(self):
		res = self.client().post('/vintners/2/vino/create', data=self.test_vino, headers={"Authorization": f'bearer none'})
		data = (res.data)
		self.assertEqual(res.status_code, 401)

# Get edit wine form test set
# RBAC - with edit permissions
	def test_get_edit_wine_by_manager(self):
		res = self.client().get('/wines/2/edit', headers={"Authorization": f'bearer {self.cellar_admin}'})
		data = res.data
		self.assertEqual(res.status_code, 200)

# RBAC - no auth edit permissions
	def test_get_edit_wine_no_auth(self):
		res = self.client().get('/wines/2/edit', headers={"Authorization": f'bearer none'})
		data = res.data
		self.assertEqual(res.status_code, 401)

# Post edit vintner form test set
	def test_update_wine(self):
		res = self.client().post('/wines/3/edit', data=self.test_vino, headers={'Authorization': 'bearer ' + self.cellar_admin}, follow_redirects=True)
		data = (res.data)
		self.assertEqual(res.status_code, 200)
		self.assertTrue(re.search('successfully edited!', res.get_data(as_text=True)))

	def test_update_wine_badurl(self):
		res = self.client().post('/wines/2000/edit', data=self.test_vino, headers={'Authorization': 'bearer ' + self.cellar_admin})
		data = (res.data)
		self.assertEqual(res.status_code, 302)
		self.assertFalse(re.search('An error occurred.',
                    res.get_data(as_text=True)))

# Delete vintner test sets
# RBAC - no permission auth test for delete : vintner by Manager Role
	def test_delete_wine_no_rbac(self):
		id = 1
		res = self.client().delete(f'/wines/{id}', headers={"Authorization": f'bearer {self.cellar_manager}'}, follow_redirects=True)
		self.assertEqual(res.status_code, 401)

# RBAC - with permission auth test for delete : vintner by Admin Role
	def test_delete_wine(self):
		id = 1
		res = self.client().delete(f'/wines/{id}', headers={"Authorization": f'bearer {self.cellar_admin}'}, follow_redirects=True)
		data = (res.data)
		vino = Vino.query.filter(Vino.id == id).one_or_none()
		self.assertEqual(res.status_code, 200)
		self.assertEqual(vino, None)

	def test_delete_wine_does_not_exist(self):
		res = self.client().delete('/wines/1000', headers={"Authorization": f'bearer {self.cellar_admin}'})
		# redirect for out of range url call
		self.assertEqual(res.status_code, 302)






# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()
