# api/v2_api.py
from django.http import HttpResponse

from portfolioapp.apps.portfolios.models import Portfolio

def get_portfolios(request):
    return HttpResponse('hello', mimetype='application/json')