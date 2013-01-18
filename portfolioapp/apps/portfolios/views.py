from django.shortcuts import render, get_object_or_404

from portfolioapp.apps.portfolios.models import Portfolio, Holding, Transaction

def portfolio_index(request):
    portfolio_list = Portfolio.objects.order_by('name')
    context = {'portfolio_list': portfolio_list}
    return render(request, 'portfolios/index.html', context)


def portfolio_detail(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    return render(request, 'portfolios/detail.html', {'portfolio': portfolio})


def holding_index(request, portfolio_id):
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    holding_list = portfolio.holding_set.all()
    context = {'holding_list': holding_list}
    return render(request, 'holdings/index.html', context)


def transaction_index(request, portfolio_id, holding_id):
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    holding = portfolio.holding_set.get(pk=holding_id)
    transaction_list = holding.transaction_set.all()
    context = {'transaction_list': transaction_list }
    return render(request, 'transactions/index.html', context)
