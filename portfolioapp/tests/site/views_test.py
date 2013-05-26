# site/views_test.py

import nose.tools as nt
from django.test import Client


class TestSiteViews(object):

    def setup(self):
        "test common views"
        self.client = Client()


    # test for existence of some common pages

    def test_view_home_page_succeed(self):
        print('in view_test_home_page_succeed')
        response = self.client.get('/')
        nt.assert_equal(response.status_code, 200)

    def test_view_signup_page_succeed(self):
        print('in view_test_signup_page_succeed')
        response = self.client.get('/sign-up')
        nt.assert_equal(response.status_code, 301)

    def test_view_signin_page_succeed(self):
        print('in view_test_signin_page_succeed')
        response = self.client.get('/sign-in')
        nt.assert_equal(response.status_code, 301)