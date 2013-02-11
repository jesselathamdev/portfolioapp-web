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


@user_passes_test(is_admin)
@page_template('admin/markets/stocks/item_index.html')
def stock_index2(request, template='admin/markets/stocks/index2.html', extra_context=None):
    stocks = Stock.objects.select_related('stock__name', 'stock__symbol', 'market__acr').order_by('name')
    context = {'stocks': stocks,}

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=RequestContext(request))


@user_passes_test(is_admin)
def stock_index3(request):
    stocks = Stock.objects.select_related('stock__name', 'stock__symbol', 'market__acr').order_by('name')
    items = get_pagination_page(1)
    return render(request, 'admin/markets/stocks/index3.html', {'stocks': stocks, 'items': items})


def get_pagination_page(page=1):
    items = Stock.objects.select_related('stock__name', 'stock__symbol', 'market__acr').order_by('name')
    paginator = Paginator(items, 10)
    try:
        page = int(page)
    except ValueError:
        page = 1

    try:
        items = paginator.page(page)
    except (EmptyPage, InvalidPage):
        items = paginator.page(paginator.num_pages)

    return items