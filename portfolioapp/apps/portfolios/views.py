# portfolios/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Portfolio, Holding, Transaction
from .forms import CreateHolding

@login_required
def portfolio_index(request):
    portfolios = Portfolio.objects.detailed_view(request.user.id)
    return render(request, 'portfolios/portfolios/index.html', {'portfolios': portfolios})


@login_required
def holding_index(request, portfolio_id):
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    holdings = Holding.objects.detailed_view(portfolio_id)
    return render(request, 'portfolios/holdings/index.html', {'portfolio': portfolio, 'holdings': holdings})


@login_required
def transaction_index(request, portfolio_id, holding_id):
    holding = Holding.objects.select_related('portfolio').get(pk=holding_id)
    transactions = Transaction.objects.select_related('portfolio', 'portfolio__holding').filter(holding__id=holding_id).order_by('-date_transacted')
    return render(request, 'portfolios/transactions/index.html', {'holding': holding, 'transactions': transactions})


@login_required
def transaction_list_index(request):
    transactions = Transaction.objects.select_related('holding__market__name', 'holding__stock__name', 'holding__stock__symbol', 'type', 'date_transacted', 'quantity', 'value').filter(holding__portfolio__user_id=request.user).order_by('date_transacted')
    return render(request, 'portfolios/transactions/index_global.html', {'transactions': transactions})


@login_required
def portfolio_detail(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    return render(request, 'portfolios/portfolios/detail.html', {'portfolio': portfolio})


@login_required
def holding_create(request, portfolio_id):
    portfolio = Portfolio.objects.get(pk=portfolio_id)

    if request.method == "POST":
        form = CreateHolding(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('holding_index'))
    else:
        form = CreateHolding()
        return render(request, 'portfolios/holdings/detail.html', {'portfolio': portfolio, 'form': form})


