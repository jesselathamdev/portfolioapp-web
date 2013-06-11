# markets/views.py

import time
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, RequestContext, get_object_or_404, render
from django.db.models import Q, Min, Max

from endless_pagination.decorators import page_template

from portfolioapp.apps.core import settings
from .models import Stock, StockPriceHistory
from .forms import StockSearchForm


######################## STOCK LIST (/stocks)

@login_required
@page_template('markets/stocks/index_paged_content.html')
def stock_index(request, template='markets/stocks/index.html', extra_context=None):
    stocks = Stock.objects.select_related('stock__name', 'stock__symbol', 'market__acr').order_by('name')

    if request.method == 'POST':
        form = StockSearchForm(request.POST)

        if form.is_valid():
            stock_id = form.cleaned_data['stock_id']
            search_term = form.cleaned_data['search_term']

            if stock_id:
                stocks = Stock.objects.select_related('stock__name', 'stock__symbol', 'market__acr').filter(id=stock_id).order_by('name')
            elif search_term:
                stocks = Stock.objects.select_related('stock__name', 'stock__symbol', 'market__acr').filter(Q(name__icontains=search_term) | Q(symbol__icontains=search_term)).order_by('name')

    else:
        form = StockSearchForm()

    context = {'stocks': stocks, 'results_per_page': settings.RESULTS_PER_PAGE, 'form': form}

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=RequestContext(request))


######################## STOCK SHOW (/stocks/:id)

@login_required
def stock_show(request, stock_id):
    stock = get_object_or_404(Stock.objects.select_related('market__acr'), pk=stock_id)
    prices_historical = StockPriceHistory.objects.filter(stock_id=stock_id, date_created__range=[date.today() - timedelta(days=365.24), date.today()]).order_by('date_created')

    if prices_historical.count() > 0:
        price_previous_day = prices_historical.reverse()[1].price_closing
        hl = prices_historical.aggregate(price_high=Max('price_high'), price_low=Min('price_low'))
        price_52_week_low = hl['price_low']
        price_52_week_high = hl['price_high']
        oldest_prices = prices_historical[0]  # oldest prices
        newest_prices = prices_historical.reverse()[0]  # newest prices
        one_year_return_percent = round(float(newest_prices.price_closing - oldest_prices.price_closing) / float(newest_prices.price_closing) * 100.00, 2)
    else:
        price_previous_day = 0.00
        price_52_week_low = 0.00
        price_52_week_high = 0.00
        one_year_return_percent = 0.00

    stock_chart = []
    for price in prices_historical:
        stock_chart.append([int(1000*time.mktime(price.date_created.timetuple())), float(price.price_closing)])

    return render(request, 'markets/stocks/show.html', {'stock': stock, 'price_previous_day': price_previous_day,
                                                        'price_52_week_low': price_52_week_low, 'price_52_week_high': price_52_week_high,
                                                        'one_year_return_percent': one_year_return_percent, 'stock_chart': stock_chart})


######################## STOCK HISTORICAL PRICE LIST (/stocks/:id/prices)

@login_required
@page_template('markets/stocks/historical_prices_index_paged_content.html')
def stock_historical_prices_index(request, stock_id, template='markets/stocks/historical_prices_index.html', extra_context=None):
    stock = get_object_or_404(Stock.objects.select_related('stock__name', 'stock__symbol', 'market__acr'), pk=stock_id)
    prices = StockPriceHistory.objects.filter(stock_id=stock_id).order_by('-date_created')

    context = {'stock': stock, 'prices': prices, 'results_per_page': settings.RESULTS_PER_PAGE}

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=RequestContext(request))
