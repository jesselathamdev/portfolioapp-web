# portfolios/api.py
from tastypie.resources import ModelResource
from .models import Market

class MarketResource(ModelResource):
    class Meta:
        queryset = Market.objects.all()[:30]
        resource_name = 'markets'