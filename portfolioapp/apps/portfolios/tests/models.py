# tests/models.py
# run with 'coverage run manage.py test --settings=portfolioapp.settings.test

from django.utils import unittest

from portfolioapp.apps.portfolios.models import Portfolio
from portfolioapp.apps.profiles.models import User

class PortfolioTestCase(unittest.TestCase):
    def setUp(self):
        u = User.objects.create(first_name='John', last_name='Smith', email='johnsmith@gmail.com', password='access')
        self.portfolio1 = Portfolio.objects.create(user=u, name='Test Portfolio 1')

    def testPortfolioName(self):
        self.assertEqual(self.portfolio1.name, 'Test Portfolio 1')
