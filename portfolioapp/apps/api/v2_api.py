# api/v2_api.py

import uuid

from django.contrib.auth import authenticate
from django.http import HttpResponse

from .forms import AuthForm
from .helpers import api_http_response, create_token, HttpMessages
from .decorators import token_required
from portfolioapp.apps.portfolios.models import Portfolio
from portfolioapp.apps.markets.models import Market


def token_create(request):
    if request.method == 'GET':  # change to POST, just playing with GET for now

        response = {
            'response': {
                'meta': {
                    'status_code': 401,  # always default to unauthorized first
                    'message': HttpMessages.UNAUTHORIZED
                }
            }
        }

        form = AuthForm(request.GET)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            identifier = form.cleaned_data['identifier']
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    token = create_token(user, identifier)

                    response['response']['meta']['status_code'] = 201
                    response['response']['meta']['message'] = HttpMessages.CREATED
                    response['response']['token'] = token
                    response['response']['identifier'] = identifier
                    response['response']['user'] = {}
                    response['response']['user']['id'] = user.id
                    response['response']['user']['first_name'] = user.first_name
                    response['response']['user']['last_name'] = user.last_name

        return api_http_response(request, response)


@token_required
def get_portfolios(request, user):
    if request.method == 'GET':
        portfolios = list(Portfolio.objects.filter(user_id=user.id).values('id', 'name', 'date_created').order_by('name'))
        response = {
            'response': {
                'meta': {
                    'status_code': 200,
                    'message': HttpMessages.OK
                },
                'portfolios': portfolios
            }
        }
        return api_http_response(request, response)


@token_required
def get_markets(request, user):
    if request.method == 'GET':
        markets = list(Market.objects.all().values('id', 'name', 'date_created'))
        response = {
            'response': {
                'meta': {
                    'status_code': 200,
                    'message': HttpMessages.OK
                },
                'markets': markets
            }
        }
        return api_http_response(request, response)