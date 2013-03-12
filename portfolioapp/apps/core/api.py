# portfolios/api.py
from django.conf.urls import url

from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from tastypie.resources import csrf_exempt

from portfolioapp.apps.portfolios.models import Portfolio
from portfolioapp.apps.markets.models import Market


# define some common and shared parameters for the model resources further down
class CommonMeta:
    authentication = BasicAuthentication()
    list_allowed_methods = ['get']


class PortfolioResource(ModelResource):
    class Meta:
        queryset = Portfolio.objects.all()
        resource_name = 'portfolios'
        authentication = BasicAuthentication()
        list_allowed_methods = ['get']

    def apply_authorization_limits(self, request, object_list):
        print("in apply_limits")
        return object_list.filter(user_id=request.user.id)


class MarketResource(ModelResource):
    class Meta(CommonMeta):
        queryset = Market.objects.all()
        resource_name = 'markets'