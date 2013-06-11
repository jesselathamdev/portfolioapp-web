# portfolios/views.py

import time
from datetime import date, timedelta

from django.shortcuts import render, render_to_response, get_object_or_404, get_list_or_404, RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Max, Min

from endless_pagination.decorators import page_template

from portfolioapp.apps.core import settings
from portfolioapp.apps.cash.models import Cash
from portfolioapp.apps.markets.models import Stock, StockPriceHistory

from .models import Portfolio, PortfolioDetail, PortfolioHolding, Holding, Transaction, Activity
from .forms import CreatePortfolioForm, CreateHoldingForm, CreateTransactionForm


######################## PORTFOLIOS

@login_required
def portfolios_index(request):
    portfolios = PortfolioDetail.objects.filter(user_id=request.user.id)
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

    return HttpResponseRedirect(reverse('portfolios_index'))


@login_required
def portfolio_delete(request, portfolio_id):
    p = Portfolio.objects.get(pk=portfolio_id)
    p.delete()

    return HttpResponseRedirect(reverse('portfolios_index'))


######################## PORTFOLIO HOLDINGS

@login_required
def portfolio_holdings_index(request, portfolio_id):
    # do this check once at the start of the request
    portfolio = get_object_or_404(Portfolio, user_id=request.user.id, id=portfolio_id)

    # don't do a 404 check here with user and portfolio id as we want to be able to still see a list page displaying cash even if the user does not have any holdings (yet)
    portfolio_holdings = PortfolioHolding.objects.filter(user_id=request.user.id, portfolio_id=portfolio_id)

    cash_summary = Cash.objects.summary_view(request.user.id, portfolio_id)

    holding_chart = []
    other_value = 0
    for holding in portfolio_holdings:
        if holding.portfolio_makeup_percent >= 4:
            holding_list = [str(holding.stock_symbol), float(round(holding.portfolio_makeup_percent, 1))]
            holding_chart.append(holding_list)
        else:
            other_value += holding.portfolio_makeup_percent

    if other_value > 0:
        holding_chart.append(['Other', float(round(other_value, 1))])

    holding_form = CreateHoldingForm()
    transaction_form = CreateTransactionForm()

    return render(request, 'portfolios/holdings/index.html', {'portfolio': portfolio, 'holdings': portfolio_holdings, 'holding_chart': holding_chart, 'cash_summary': cash_summary, 'holding_form': holding_form, 'transaction_form': transaction_form})


@login_required
def portfolio_holding_show(request, portfolio_id, holding_id):
    holding = get_object_or_404(Holding.objects.select_related('holding', 'portfolio', 'stock', 'stock__market'), portfolio__user_id=request.user.id, portfolio_id=portfolio_id, id=holding_id)
    holding_transaction_count = Transaction.objects.filter(holding__id=holding_id).count()

    prices_historical = StockPriceHistory.objects.filter(stock_id=holding.stock_id, date_created__range=[date.today() - timedelta(days=365.24), date.today()]).order_by('date_created')

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

    return render(request, 'portfolios/holdings/show.html', {'holding': holding, 'holding_transaction_count': holding_transaction_count,
                                                             'stock': holding.stock, 'price_previous_day': price_previous_day,
                                                             'price_52_week_low': price_52_week_low, 'price_52_week_high': price_52_week_high,
                                                             'one_year_return_percent': one_year_return_percent, 'stock_chart': stock_chart})


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
            print('form was invalid')
            messages.info(request, form.errors)

    return HttpResponseRedirect(reverse('portfolio_holdings_index', args=(int(portfolio_id),)))


@login_required
def holding_delete(request, portfolio_id, holding_id):
    h = Holding.objects.get(pk=holding_id)

    h.delete()

    return HttpResponseRedirect(reverse('portfolio_holdings_index', args=(int(portfolio_id),)))


######################## PORTFOLIO HOLDING TRANSACTIONS

@login_required
@page_template('portfolios/transactions/index_paged_content.html')
def transactions_index(request, portfolio_id, holding_id, template='portfolios/transactions/index.html', extra_context=None):
    holding = get_object_or_404(Holding.objects.select_related('holding', 'holding__portfolio'), portfolio__user_id=request.user.id, id=holding_id)
    transactions = get_list_or_404(Transaction.objects.select_related('holding', 'holding__portfolio').order_by('-date_transacted'), holding__portfolio__user_id=request.user.id, holding__portfolio__id=portfolio_id, holding__id=holding_id)

    context = {'holding': holding, 'transactions': transactions, 'results_per_page': settings.RESULTS_PER_PAGE}

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def transaction_create(request, portfolio_id, holding_id):
    if request.is_ajax():
        if request.method == 'POST':
            form = CreateTransactionForm(request.POST)

            response = {
                'data': 'success'
            }

            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully added transaction.')
            else:
                messages.error(request, 'There was a problem adding the transaction.')

    return HttpResponse(response)


######################## TRANSACTION ACTIVITY

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