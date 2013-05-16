# markets/api.py
# views for api

import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q

from .models import Stock


######################## INTERNAL, SUPPORTS STOCK TYPEAHEAD ON /ADMIN/STOCKS

@login_required
def stock_index(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        stocks = Stock.objects.select_related().filter(Q(name__icontains = q) | Q(symbol__icontains = q))[:10]
        results = []
        for stock in stocks:
            stock_json = {}
            stock_json['id'] = stock.id
            stock_json['value'] = '%s (%s:%s)' % (stock.name, stock.symbol, stock.market.acr)
            results.append(stock_json)
        data = json.dumps(results)
    else:
        data = 'fail'

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


######################## INTERNAL, SUPPORTS STOCK TYPEAHEAD ON /STOCKS

@login_required
def stock_index2(request):
    if request.is_ajax():
        q = request.GET.get('q', '')
        stocks = Stock.objects.select_related().filter(Q(name__icontains = q) | Q(symbol__icontains = q))[:10]
        results = []
        for stock in stocks:
            stock_json = {}
            stock_json['id'] = stock.id
            stock_json['value'] = '%s (%s:%s)' % (stock.name, stock.symbol, stock.market.acr)
            stock_json['displayValue'] = '%s (%s:%s)' % (stock.name, stock.symbol, stock.market.acr)
            stock_json['name'] = stock.name
            stock_json['symbol'] = stock.symbol
            stock_json['acr'] = stock.market.acr
            stock_json['last_price'] = str(stock.last_price)
            results.append(stock_json)
        data = json.dumps(results)
    else:
        data = 'fail'

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)