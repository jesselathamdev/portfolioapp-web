# admin/view.py
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
def stock_index2(request):
    stocks = Stock.objects.select_related('stock__name', 'stock__symbol', 'market__acr').order_by('name')

    return render(request, 'admin/markets/stocks/index.html', {'stocks': stocks})