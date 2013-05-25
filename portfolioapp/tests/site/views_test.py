# site/views_test.py

import nose.tools as nt
from django.test import Client


class TestSiteViews(object):

    def setup(self):
        "test common views"
        self.client = Client()


    # test for existence of some common pages

    def test_home_page(self):
        response = self.client.get('/')
        nt.assert_equal(response.status_code, 200)

    def test_signup_page(self):
        response = self.client.get('/sign-up')
        nt.assert_equal(response.status_code, 301)

    def test_signin_page(self):
        response = self.client.get('/sign-in')
        nt.assert_equal(response.status_code, 301)