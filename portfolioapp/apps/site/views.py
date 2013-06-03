# site/views.py

from django.shortcuts import render

from portfolioapp.apps.portfolios.models import PortfolioDetail
from portfolioapp.apps.portfolios.models import Activity


def site_index(request):
    if request.user.is_authenticated():
        portfolios = PortfolioDetail.objects.filter(user_id=request.user.id).order_by('name')
        recent_activity = Activity.objects.select_related('portfolio', 'stock', 'stock__market').filter(user_id=request.user.id).order_by('-date_transacted')[0:4]

        return render(request, 'site/site_index.html', {'portfolios': portfolios, 'recent_activity': recent_activity})

    return render(request, 'site/site_index.html')

