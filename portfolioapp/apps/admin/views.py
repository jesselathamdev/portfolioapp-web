# admin/view.py
from django.shortcuts import render, render_to_response, RequestContext, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.contrib import messages

from endless_pagination.decorators import page_template

from portfolioapp.apps.core import settings
from portfolioapp.apps.core.decorators import is_admin
from portfolioapp.apps.markets.models import Stock, Market
from .forms import EditStockForm

@user_passes_test(is_admin)
def home_index(request):
    return render(request, 'admin/index.html', {})


# the following uses django-endless-pagination for pagination routines; less messy in terms of set up and configuration but
# only does pagination
@user_passes_test(is_admin)
@page_template('admin/markets/stocks/index_paged_content.html')
def stock_index(request, template='admin/markets/stocks/index.html', extra_context=None):
    stocks = Stock.objects.select_related('stock__name', 'stock__symbol', 'market__acr').order_by('name')
    context = {'stocks': stocks, 'results_per_page': settings.RESULTS_PER_PAGE,}

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=RequestContext(request))


@user_passes_test(is_admin)
def stock_edit(request, stock_id):
    stock = Stock.objects.get(pk=stock_id)

    if request.method == 'POST':
        form = EditStockForm(request.POST, instance=stock)
        if form.is_valid():
            # return HttpResponse(form)
            form.save()
            messages.success(request, 'Your form was saved.')
            return HttpResponseRedirect(reverse('admin_stock_index'))
        else:
            return render(request, 'admin/markets/stocks/edit.html', {'stock': stock, 'form': form})
    else:
        form = EditStockForm(instance=stock)
        return render(request, 'admin/markets/stocks/edit.html', {'stock': stock, 'form': form})


@user_passes_test(is_admin)
def market_index(request):
    markets = Market.objects.annotate(stock_count=Count('stock'))

    return render(request, 'admin/markets/markets/index.html', {'markets': markets})