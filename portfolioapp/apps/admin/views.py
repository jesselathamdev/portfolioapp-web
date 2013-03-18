# admin/view.py
from django.shortcuts import render, render_to_response, RequestContext, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.contrib import messages
from django.db.models import Q

from endless_pagination.decorators import page_template

from portfolioapp.apps.core import settings
from portfolioapp.apps.core.decorators import is_admin
from portfolioapp.apps.markets.models import Stock, Market
from portfolioapp.apps.profiles.models import User
from portfolioapp.apps.profiles.forms import AdminEditUserProfileForm
from portfolioapp.apps.api.models import ApiLog
from .forms import StockEditForm, StockSearchForm


@user_passes_test(is_admin)
def home_index(request):
    return render(request, 'admin/index.html', {})


@user_passes_test(is_admin)
@page_template('admin/markets/stocks/index_paged_content.html')
def stock_index(request, template='admin/markets/stocks/index.html', extra_context=None):
    if request.method == 'POST':
        search_form = StockSearchForm(request.POST)
        if search_form.is_valid():
            term = search_form.cleaned_data['search_term']
            stocks = Stock.objects.select_related('stock__name', 'stock__symbol', 'market__acr').filter(Q(name__icontains=term)).order_by('name')
        else:
            stocks = Stock.objects.select_related('stock__name', 'stock__symbol', 'market__acr').order_by('name')

        context = {'stocks': stocks, 'results_per_page': settings.RESULTS_PER_PAGE, 'search_form': search_form}

        if extra_context is not None:
            context.update(extra_context)

        return render_to_response(template, context, context_instance=RequestContext(request))

    else:
        stocks = Stock.objects.select_related('stock__name', 'stock__symbol', 'market__acr').order_by('name')

        search_form = StockSearchForm()

        context = {'stocks': stocks, 'results_per_page': settings.RESULTS_PER_PAGE, 'search_form': search_form}

        if extra_context is not None:
            context.update(extra_context)

        return render_to_response(template, context, context_instance=RequestContext(request))


@user_passes_test(is_admin)
def stock_edit(request, stock_id):
    stock = Stock.objects.get(pk=stock_id)

    if request.method == 'POST':
        if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('admin_stock_index'))

        form = StockEditForm(request.POST, instance=stock)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your form was saved.')
            return HttpResponseRedirect(reverse('admin_stock_index'))
        else:
            return render(request, 'admin/markets/stocks/edit.html', {'stock': stock, 'form': form})
    else:
        form = StockEditForm(instance=stock)
        return render(request, 'admin/markets/stocks/edit.html', {'stock': stock, 'form': form})


@user_passes_test(is_admin)
def market_index(request):
    markets = Market.objects.annotate(stock_count=Count('stock'))
    return render(request, 'admin/markets/markets/index.html', {'markets': markets})


@user_passes_test(is_admin)
def profile_index(request):
    users = User.objects.all().order_by('email')
    return render(request, 'admin/profiles/index.html', {'users': users})


@user_passes_test(is_admin)
def profile_edit(request, user_id):
    user = User.objects.get(pk=user_id)

    if request.method == 'POST':
        if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('admin_profile_index'))

        form = AdminEditUserProfileForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile saved successfully.')
            return HttpResponseRedirect(reverse('admin_profile_index'))
    else:
        form = AdminEditUserProfileForm(instance=user)
        return render(request, 'admin/profiles/edit.html', {'form': form, 'user': user})


@user_passes_test(is_admin)
@page_template('admin/api/index_paged_content.html')
def api_log_index(request, template='admin/api/index.html', extra_context=None):
    apilog = ApiLog.objects.all().order_by('-date_created')

    context = {'apilog': apilog, 'results_per_page': settings.RESULTS_PER_PAGE}

    if extra_context is not None:
            context.update(extra_context)

    return render_to_response(template, context, context_instance=RequestContext(request))