from django.shortcuts import render

from holdings.models import Holding

def index(request, portfolio_id):
    holding_list = Holding.objects.filter(portfolio_id=portfolio_id)
    context = {"holding_list": holding_list}
    return render(request, 'holdings/index.html', context)