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
    class Meta(CommonMeta):
        queryset = Portfolio.objects.all()
        resource_name = 'portfolios'

    def apply_limits(self, request, object_list):
        return object_list.filter(user_id=request.user.id)

    # def prepend_urls(self):
    #     """
    #     Returns a URL scheme based on the default scheme to specify
    #     the response format as a file extension, e.g. /api/v1/users.json
    #     """
    #     return [
    #         url(r"^(?P<resource_name>%s)\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('dispatch_list'), name="api_dispatch_list"),
    #         url(r"^(?P<resource_name>%s)/schema\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('get_schema'), name="api_get_schema"),
    #         url(r"^(?P<resource_name>%s)/set/(?P<pk_list>\w[\w/;-]*)\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('get_multiple'), name="api_get_multiple"),
    #         url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
    #     ]
    #
    # def determine_format(self, request):
    #     """
    #     Used to determine the desired format from the request.format
    #     attribute.
    #     """
    #     if (hasattr(request, 'format') and
    #             request.format in self._meta.serializer.formats):
    #         return self._meta.serializer.get_mime_for_format(request.format)
    #     return super(PortfolioResource, self).determine_format(request)
    #
    # def wrap_view(self, view):
    #     @csrf_exempt
    #     def wrapper(request, *args, **kwargs):
    #         request.format = kwargs.pop('format', None)
    #         wrapped_view = super(PortfolioResource, self).wrap_view(view)
    #         return wrapped_view(request, *args, **kwargs)
    #     return wrapper


class MarketResource(ModelResource):
    class Meta(CommonMeta):
        queryset = Market.objects.all()
        resource_name = 'markets'