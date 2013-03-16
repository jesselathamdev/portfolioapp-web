# api/v2_api.py

from .helpers import api_http_response

from portfolioapp.apps.portfolios.models import Portfolio
from portfolioapp.apps.markets.models import Market


def get_portfolios(request):
    if request.method == 'GET':
        portfolios = list(Portfolio.objects.filter(user_id=2).values('id', 'name', 'date_created').order_by('name'))
        response = {
            'response': {
                'head': {
                    'status_code': 200
                },
                'portfolios': portfolios
            }
        }
        return api_http_response(request, response)


def get_markets(request):
    if request.method == 'GET':
        markets = list(Market.objects.all().values('id', 'name', 'date_created'))
        response = {
            'response': {
                'head': {
                    'status_code': 200
                },
                'markets': markets
            }
        }
        return api_http_response(request, response)