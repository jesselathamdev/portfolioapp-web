# markets/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, RequestContext

from endless_pagination.decorators import page_template

from portfolioapp.apps.core import settings
from .models import Stock


@login_required
@page_template('admin/markets/stocks/index_paged_content.html')
def stock_index(request, template='markets/stocks/index.html', extra_context=None):
    stocks = Stock.objects.select_related('stock__name', 'stock__symbol', 'market__acr').order_by('name')

    context = {'stocks': stocks, 'results_per_page': settings.RESULTS_PER_PAGE}

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=RequestContext(request))