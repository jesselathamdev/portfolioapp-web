# markets/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, RequestContext
from django.db.models import Q

from endless_pagination.decorators import page_template

from portfolioapp.apps.core import settings
from .models import Stock
from .forms import StockSearchForm


@login_required
@page_template('admin/markets/stocks/index_paged_content.html')
def stock_index(request, template='markets/stocks/index.html', extra_context=None):
    stocks = Stock.objects.select_related('stock__name', 'stock__symbol', 'market__acr').order_by('name')

    if request.method == 'POST':
        form = StockSearchForm(request.POST)

        if form.is_valid():
            stock_id = form.cleaned_data['stock_id']
            search_term = form.cleaned_data['search_term']

            print('form is valid')

            if stock_id:
                print('found stock id')
                stocks = Stock.objects.select_related('stock__name', 'stock__symbol', 'market__acr').filter(id=stock_id).order_by('name')
            elif search_term:
                print('found search term')
                stocks = Stock.objects.select_related('stock__name', 'stock__symbol', 'market__acr').filter(Q(name__icontains = search_term) | Q(symbol__icontains = search_term)).order_by('name')
            else:
                print('stock_id: %s; search_term: %s' % (stock_id, search_term))

        else:
            print('error: %s' % form.errors)

    else:
        form = StockSearchForm()

    context = {'stocks': stocks, 'results_per_page': settings.RESULTS_PER_PAGE, 'form': form}

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=RequestContext(request))