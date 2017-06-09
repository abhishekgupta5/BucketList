# test_bucketlist.py
import unittest
import os
import json
from app import create_app, db

class BucketlistTestCase(unittest.TestCase):

    def setUp(self):
        #Define test variables and inititalize app
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Go to mountains soon'}

        #Binds the app with current context
        with self.app.app_context():
            db.create_all()

    def test_bucketlist_creation(self):
        """Test API can create a bucketlist (POST request)"""
        res = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('to mountains', str(res.data))

    def test_api_can_get_all_bucketlists(self):
        """Test API can get a bucketlist (GET request)"""
        res = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/bucketlists/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('to mountains', str(res.data))

    def test_api_can_get_bucketlist_by_id(self):
        rv = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get('/bucketlists/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('to mountains', str(result.data))

    def test_bucketlist_can_be_edited(self):
        """Test API can edit an existing API (PUT request)"""
        rv = self.client().post('/bucketlists/', data={'name':'Code, Travel and Startup'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put('/bucketlists/1', data={'name':'You know what to do'})
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/bucketlists/1')
        self.assertIn('know what', str(results.data))

    def test_bucketlist_deletion(self):
        """Test API can delete an existing bucketlist (DELETE request)"""
        rv = self.client().post('/bucketlists/', data={'name':'Code, Travel and Startup'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/bucketlists/1')
        self.assertEqual(res.status_code, 200)
        #Test to see if it exist, should return a 404
        result = self.client().get('/bucketlists/1')
        self.assertEqual(result.status_code, 404)

    def teardown(self):
        """Teardown all initialized variables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()



