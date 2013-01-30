# portfolios/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Portfolio, Holding, Transaction
from .forms import CreateHolding

@login_required
def portfolio_index(request):
    # TODO: remove old queries below
    # portfolio_list = Portfolio.objects.filter(user=request.user).annotate(num_holdings=Count('holding')).order_by('name')
    # portfolios = Portfolio.objects.filter(user_id=request.user.id).annotate(total_price=Sum('holding__transaction__price')).order_by('name')

    portfolios = Portfolio.objects.detailed_view(request.user.id)
    Portfolio.objects.detailed_view()

    return render(request, 'portfolios/index.html', {'portfolios': portfolios})


@login_required
def portfolio_detail(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)

    return render(request, 'portfolios/detail.html', {'portfolio': portfolio})


@login_required
def holding_index(request, portfolio_id):
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    holdings = Holding.objects.current_activity(request.user.id)

    return render(request, 'holdings/index.html', {'portfolio': portfolio, 'holdings': holdings})


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
        return render(request, 'holdings/detail.html', {'portfolio': portfolio, 'form': form})


@login_required
def transaction_index(request, portfolio_id, holding_id):
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    holding = Holding.objects.get(pk=holding_id)
    transaction_list = holding.transaction_set.all().order_by('date_created')

    return render(request, 'transactions/index.html', {'portfolio': portfolio, 'holding': holding, 'transaction_list': transaction_list})


@login_required
def transaction_list_index(request):
    # the following is great as it returns a small subset for what's needed, but then you can't use the magic function of .get_category_id_display; use .select_related instead
    # transaction_list = Transaction.objects.values('holding__name', 'holding__market', 'holding__symbol', 'category_id', 'date_created', 'quantity', 'price').filter(holding__portfolio__user_id=request.user).order_by('date_created')
    # holdings = Holding.objects.filter(portfolio__user_id=2).annotate(total_price=Sum('transaction__price'))
    transaction_list = Transaction.objects.select_related('holding__name', 'holding__market', 'holding__symbol', 'type', 'date_created', 'quantity', 'price').filter(holding__portfolio__user_id=request.user).order_by('date_created')

    return render(request, 'transactions/list_index.html', {'transaction_list': transaction_list})