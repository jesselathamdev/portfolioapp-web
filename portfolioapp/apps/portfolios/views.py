# portfolios/views.py
from django.shortcuts import render, render_to_response, get_object_or_404, RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from endless_pagination.decorators import page_template

from portfolioapp.apps.core import settings
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
def holding_create(request, portfolio_id):
    portfolio = Portfolio.objects.get(pk=portfolio_id)

    if request.method == 'POST':
        form = CreateHolding(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your form was saved.')
            return HttpResponseRedirect(reverse('holding_index', args=(portfolio_id,)))
        else:
            return render(request, 'portfolios/holdings/create.html', {'form': form})
    else:
        form = CreateHolding()
        return render(request, 'portfolios/holdings/create.html', {'portfolio': portfolio, 'form': form })


@login_required
def transaction_index(request, portfolio_id, holding_id):
    holding = Holding.objects.select_related('portfolio').get(pk=holding_id)
    transactions = Transaction.objects.select_related('portfolio', 'portfolio__holding').filter(holding__id=holding_id).order_by('-date_transacted')
    return render(request, 'portfolios/transactions/index.html', {'holding': holding, 'transactions': transactions})


@login_required
@page_template('portfolios/transactions/index_global_paged_content.html')
def transaction_global_index(request, template='portfolios/transactions/index_global.html', extra_context=None):
    transactions = Transaction.objects.select_related('holding__stock__name', 'holding__stock__symbol', 'holding__stock__market__acr', 'type', 'date_transacted', 'quantity', 'value').filter(holding__portfolio__user_id=request.user).order_by('-date_transacted')
    context = {'transactions': transactions, 'results_per_page': settings.RESULTS_PER_PAGE}

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def portfolio_detail(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    return render(request, 'portfolios/portfolios/detail.html', {'portfolio': portfolio})


#@login_required
#def holding_create(request, portfolio_id):
#    portfolio = Portfolio.objects.get(pk=portfolio_id)
#
#    if request.method == "POST":
#        form = CreateHolding(request.POST)
#        if form.is_valid():
#            form.save()
#            return HttpResponseRedirect(reverse('holding_index'))
#    else:
#        form = CreateHolding()
#        return render(request, 'portfolios/holdings/detail.html', {'portfolio': portfolio, 'form': form})


