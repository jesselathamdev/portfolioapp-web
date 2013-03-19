# api/v2_api.py

import uuid

from django.contrib.auth import authenticate
from django.http import HttpResponse

from .forms import AuthForm
from .helpers import api_http_response, create_token
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


def token_create(request):
    if request.method == 'GET': # change to POST, just playing with GET for now
        token = ''
        form = AuthForm(request.GET)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    token = create_token(user)

        response = {
            'response': {
                'head': {
                    'status_code': 201 # assuming success for initial case
                },
                'token': token
            }
        }
        return api_http_response(request, response)