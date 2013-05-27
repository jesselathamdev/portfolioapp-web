# markets/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, RequestContext, get_object_or_404, render
from django.db.models import Q

from endless_pagination.decorators import page_template

from portfolioapp.apps.core import settings
from .models import Stock, StockPriceHistory
from .forms import StockSearchForm


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
                stocks = Stock.objects.select_related('stock__name', 'stock__symbol', 'market__acr').filter(Q(name__icontains = search_term) | Q(symbol__icontains = search_term)).order_by('name')

    else:
        form = StockSearchForm()

    context = {'stocks': stocks, 'results_per_page': settings.RESULTS_PER_PAGE, 'form': form}

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def stock_show(request, stock_id):
    stock = get_object_or_404(Stock.objects.select_related('market__acr'), pk=stock_id)

    return render(request, 'markets/stocks/show.html', {'stock': stock})


@login_required
@page_template('markets/stocks/historical_prices_index_paged_content.html')
def stock_historical_prices_index(request, stock_id, template='markets/stocks/historical_prices_index.html', extra_context=None):
    stock = get_object_or_404(Stock.objects.select_related('stock__name', 'stock__symbol', 'market__acr'), pk=stock_id)
    prices = StockPriceHistory.objects.filter(stock_id=stock_id).order_by('-date_created')

    context = {'stock': stock, 'prices': prices, 'results_per_page': settings.RESULTS_PER_PAGE}

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=RequestContext(request))
