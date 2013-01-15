from django.shortcuts import render, get_object_or_404

from portfolioapp.apps.portfolios.models import Portfolio

def index(request):
    portfolio_list = Portfolio.objects.order_by('name')

    context = {
        'portfolio_list': portfolio_list
    }

    return render(request, 'portfolios/index.html', context)


def detail(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)

    return render(request, 'portfolios/detail.html', {'portfolio': portfolio})
