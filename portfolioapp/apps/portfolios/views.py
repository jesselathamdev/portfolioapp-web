from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from .forms import CreateHolding

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
    #holdings = portfolio.holding_set.all().order_by('name')

#    holdings = Holding.objects.filter(portfolio__user_id=request.user).annotate(total_quantity=Count('transaction__id'), total_price=Sum('transaction__price')).order_by('name')
    # the problem with the above is that aggregate/annotate functions are returning None instead of 0 for grouping, sucky.
    # but now after thinking about it the control can just be done in the template

    holdings = Holding.objects.raw('''SELECT ph.id, ph.name, ph.market, ph.symbol, COALESCE(COUNT(pt.id), 0) as total_quantity, COALESCE(SUM(pt.price), 0) as total_price, (COALESCE(COUNT(pt.id), 0) * COALESCE(SUM(pt.price), 0)) as book_value
                                         FROM portfolios_holding ph
                                         LEFT JOIN portfolios_transaction pt
                                           ON ph.id = pt.holding_id
                                         INNER JOIN portfolios_portfolio pp
                                           ON pp.id = ph.portfolio_id
                                         WHERE pp.user_id = %s
                                         GROUP BY ph.id
                                         ORDER BY ph.name''' % request.user.id)

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
    transaction_list = Transaction.objects.select_related('holding__name', 'holding__market', 'holding__symbol', 'category_id', 'date_created', 'quantity', 'price').filter(holding__portfolio__user_id=request.user).order_by('date_created')

    return render(request, 'transactions/list_index.html', {'transaction_list': transaction_list})