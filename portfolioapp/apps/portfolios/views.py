# portfolios/views.py

from django.shortcuts import render, render_to_response, get_object_or_404, RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Sum

from endless_pagination.decorators import page_template

from portfolioapp.apps.core import settings
from portfolioapp.apps.cash.models import Cash
from portfolioapp.apps.cash.managers import CashManager
from .models import Portfolio, Holding, Transaction, Activity
from .forms import CreatePortfolioForm, CreateHoldingForm


@login_required
def portfolio_index(request):
    portfolios = Portfolio.objects.summary_view(request.user.id)
    form = CreatePortfolioForm()
    return render(request, 'portfolios/portfolios/index.html', {'portfolios': portfolios, 'form': form})


@login_required
def portfolio_create(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data['user'] = request.user.id

        form = CreatePortfolioForm(data)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your portfolio %s was created.' % form.cleaned_data['name'])
        else:
            messages.error(request, 'There was an error creating your portfolio.')

    return HttpResponseRedirect(reverse('portfolio_index'))


@login_required
def portfolio_delete(request, portfolio_id):
    p = Portfolio.objects.get(pk=portfolio_id)
    p.delete()
    return HttpResponseRedirect(reverse('portfolio_index'))


@login_required
def holding_index(request, portfolio_id):
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    holdings = Holding.objects.summary_view(request.user.id, portfolio_id)
    cash_summary = Cash.objects.summary_view(request.user.id, portfolio_id)

    holding_chart = []
    other_value = 0
    for holding in holdings:
        if holding.portfolio_makeup_percent >= 4:
            holding_list = [str(holding.stock_symbol), float(round(holding.portfolio_makeup_percent, 1))]
            holding_chart.append(holding_list)
        else:
            other_value += holding.portfolio_makeup_percent

    if other_value > 0:
        holding_chart.append(['Other', float(round(other_value, 1))])

    form = CreateHoldingForm()
    return render(request, 'portfolios/holdings/index.html', {'portfolio': portfolio, 'holdings': holdings, 'holding_chart': holding_chart, 'cash_summary': cash_summary, 'form': form})


@login_required
def holding_create(request, portfolio_id):
    if request.method == 'POST':
        data = request.POST.copy()
        data['portfolio'] = portfolio_id

        form = CreateHoldingForm(data)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your holding %s was created.' % form.cleaned_data['stock_name'])

        else:
            messages.info(request, form.errors)

    return HttpResponseRedirect(reverse('holding_index', args=(int(portfolio_id),)))


@login_required
def holding_delete(request, portfolio_id, holding_id):
    h = Holding.objects.get(pk=holding_id)
    h.delete()
    return HttpResponseRedirect(reverse('holding_index', args=(int(portfolio_id),)))


@login_required
@page_template('portfolios/transactions/index_paged_content.html')
def transaction_index(request, portfolio_id, holding_id, template='portfolios/transactions/index.html', extra_context=None):
    holding = Holding.objects.select_related('portfolio').get(pk=holding_id)
    transactions = Transaction.objects.select_related('portfolio', 'portfolio__holding').filter(holding__id=holding_id).order_by('-date_transacted')
    context = {'holding': holding, 'transactions': transactions, 'results_per_page': settings.RESULTS_PER_PAGE}

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@page_template('portfolios/activity/index_paged_content.html')
def activity_index(request, template='portfolios/activity/index.html', extra_context=None):
    activity = Activity.objects.filter(user_id=request.user.id).order_by('-date_transacted')
    context = {'activity': activity, 'results_per_page': settings.RESULTS_PER_PAGE}

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def portfolio_detail(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    return render(request, 'portfolios/portfolios/detail.html', {'portfolio': portfolio})