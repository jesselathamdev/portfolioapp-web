# admin/view.py
from django.shortcuts import render, render_to_response, RequestContext
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage

from endless_pagination.decorators import page_template

from portfolioapp.apps.core import settings
from portfolioapp.apps.core.decorators import is_admin
from portfolioapp.apps.markets.models import Stock

@user_passes_test(is_admin)
def home_index(request):
    return render(request, 'admin/index.html', {})


# standard django pagination with post-backs to the server for the next list set; pretty basic but it works
@user_passes_test(is_admin)
def stock_index(request):
    stocks = Stock.objects.select_related('stock__name', 'stock__symbol', 'market__acr').order_by('name')
    paginator = Paginator(stocks, settings.RESULTS_PER_PAGE)

    page = request.GET.get('page')

    try:
        paged_stocks = paginator.page(page)
    except PageNotAnInteger:
        paged_stocks = paginator.page(1)
    except EmptyPage:
        paged_stocks = paginator.page(paginator.num_pages)

    return render(request, 'admin/markets/stocks/index.html', {'stocks': paged_stocks})


# the following uses django-endless-pagination for pagination routines; less messy in terms of set up and configuration but
# only does pagination
@user_passes_test(is_admin)
@page_template('admin/markets/stocks/ep_paged_content.html')
def ep_stock_index(request, template='admin/markets/stocks/ep_index.html', extra_context=None):
    stocks = Stock.objects.select_related('stock__name', 'stock__symbol', 'market__acr').order_by('name')
    context = {'stocks': stocks, 'results_per_page': settings.RESULTS_PER_PAGE,}

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=RequestContext(request))


# the following is an implementation of django-dajax and django-dajaxice; spent a lot of time figuring it out but as a
# toolkit it allows much more than django-endless-pagination; requires an extra pagination function below as well as an
# ajax.py which generates a custom dajaxice.core.js from ./manage.py collectstatic
@user_passes_test(is_admin)
def dajax_stock_index(request):
    items = dajax_paged_stocks(1)
    return render(request, 'admin/markets/stocks/dajax_index.html', {'items': items})


def dajax_paged_stocks(page=1):
    stocks = Stock.objects.select_related('stock__name', 'stock__symbol', 'market__acr').order_by('name')
    paginator = Paginator(stocks, settings.RESULTS_PER_PAGE)

    try:
        page = int(page)
    except ValueError:
        page = 1

    try:
        items = paginator.page(page)
    except (EmptyPage, InvalidPage):
        items = paginator.page(paginator.num_pages)

    return items