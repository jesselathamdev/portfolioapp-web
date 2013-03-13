# api/v2_api.py
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

from portfolioapp.apps.portfolios.models import Portfolio
from portfolioapp.apps.markets.models import Market

def get_portfolios(request):
    if request.method == 'GET':
        portfolios = list(Portfolio.objects.filter(user_id=2).values('id', 'name', 'date_created'))
        json_portfolios = json.dumps(portfolios, cls=DjangoJSONEncoder)
        return HttpResponse(json_portfolios, mimetype='application/json', status=200)

def get_markets(request):
    if request.method == 'GET':
        markets = list(Market.objects.all().values('id', 'name', 'date_created'))
        results = {}
        results['data'] = markets
        return HttpResponse(json.dumps(results, cls=DjangoJSONEncoder), mimetype='application/json', status=200)


class JSONResponseJSONDumps(HttpResponse):
    """JSON response class."""
    def __init__(self, obj='', json_opts={}, mimetype="application/json", *args, **kwargs):
         content = json.dumps(obj, cls=DjangoJSONEncoder)
         super(JSONResponseJSONDumps, self).__init__(content, mimetype, *args, **kwargs)

# http://stackoverflow.com/questions/2428092/creating-a-json-response-using-django-and-python