from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from portfolioapp.apps.portfolios.models import Portfolio, Holding, Transaction

@login_required
def portfolio_index(request):
    portfolio_list = Portfolio.objects.filter(user=request.user).order_by('name')
    return render(request, 'portfolios/index.html', {'portfolio_list': portfolio_list, 'user': request.user})

@login_required
def portfolio_detail(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    return render(request, 'portfolios/detail.html', {'portfolio': portfolio, 'user': request.user})

@login_required
def holding_index(request, portfolio_id):
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    holding_list = portfolio.holding_set.all()
    return render(request, 'holdings/index.html', {'portfolio': portfolio, 'holding_list': holding_list, 'user': request.user})
