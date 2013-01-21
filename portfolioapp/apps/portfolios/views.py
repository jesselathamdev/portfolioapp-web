from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse

from portfolioapp.apps.portfolios.models import Portfolio, Holding, Transaction

@login_required
def portfolio_index(request):
    # the following solves for select N queries when using .holding_set.count in templates
    portfolio_list = Portfolio.objects.filter(user=request.user).annotate(num_holdings=Count('holding')).order_by('name')
    return render(request, 'portfolios/index.html', {'portfolio_list': portfolio_list})

@login_required
def portfolio_detail(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    return render(request, 'portfolios/detail.html', {'portfolio': portfolio})

@login_required
def holding_index(request, portfolio_id):
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    holding_list = portfolio.holding_set.all().order_by('name')
    return render(request, 'holdings/index.html', {'portfolio': portfolio, 'holding_list': holding_list})

@login_required
def holding_detail(request, portfolio_id, holding_id):
    strResponse = "%s %s" % (portfolio_id, holding_id)
    return HttpResponse()

@login_required
def transaction_index(request, portfolio_id, holding_id):
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    holding = Holding.objects.get(pk=holding_id)
    return render(request, 'transactions/index.html')
