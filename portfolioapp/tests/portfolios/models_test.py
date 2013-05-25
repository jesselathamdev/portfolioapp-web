# portfolios/models_test.py

import nose.tools

from portfolioapp.apps.profiles.models import User
from portfolioapp.apps.portfolios.models import Portfolio



class TestPorfolio(object):

    def setup(self):
        # u = User.objects.create(first_name='John', last_name='Smith', email='john.smith@gmail.com', password='access', confirm_password='access')
        pass

    def test_create_portfolio_succeed(self):
        u = User.objects.create(first_name='John', last_name='Smith', email='john.smith@gmail.com', password='access')
        u.save()

        p = Portfolio.objects.create(user=u, name='TestPortfolio')
        p.save()


    def test_edit_portfolio_succeed(self):
        pass

    def test_delete_portfolio_succeed(self):
        pass





